import itertools, copy

class BaseStore():
    #The parent class for MemberStore and PostStore classes
    def __init__(self, data_provider , last_id):
        self._data_provider = data_provider
        self._last_id = last_id

    def get_all(self):
        #Return all objects from data store
        return self._data_provider

    def add(self, item_instance):
        #add new item
        item_instance.id = self._last_id
        self._data_provider.append(item_instance)
        self._last_id += 1

    def get_by_id(self, id):
        #get an item by its id
        item_lst = copy.deepcopy(self.get_all())
        result = None
        for obj in item_lst:
            if obj.id == id:
                result = obj
        return result

    def update(self, item_instance):
        #update an item
        item_instance_id = item_instance.id
        item_lst = self.get_all()
        for i, item in enumerate(item_lst):
            if item.id == item_instance_id:
                item_lst[i] = item_instance

    def delete(self, id):
        #delete an item
        item_instance = self.get_by_id(id)
        self._data_provider.remove(item_instance)

    def entity_exists(self, item_instance):
        #check if this item exists in data store or not
        result = True
        if self.get_by_id(item_instance.id) is None:
            result = False
        return result


class MemberStore(BaseStore):
    #Class represents a store for all Members
    members = []
    last_id = 1

    def __init__(self):
        BaseStore.__init__(self, MemberStore.members, MemberStore.last_id)

    def get_by_name(self, name):
        #get member by name
        member_lst = copy.deepcopy(self.get_all())
        for m in member_lst:
            if m.name == name:
                yield m

    def get_members_with_posts(self, all_posts):
        #get all members but each member with all his posts
        all_members = copy.deepcopy(self.get_all())
        for m, p in itertools.product(all_members, all_posts):
            if m.id == p.member_id :
                m.posts.append(p)
        for m in all_members:
            yield m

    def get_top_ten(self, all_posts):
        members_with_post_list = self.get_members_with_posts(all_posts)
        sorted_lst = sorted(members_with_post_list, key=lambda p: len(p.posts), reverse = True)
        return sorted_lst[:2]

class PostStore(BaseStore):
    #Class represents a store for all posts
    posts = []
    last_id = 1

    def __init__(self):
        BaseStore.__init__(self, PostStore.posts, PostStore.last_id)

    def get_posts_by_date(self):
        #get all posts sorted by date starting from the newest one to the oldest one
        all_posts = self.get_all()
        all_posts.sort(key=lambda p: p.date, reverse=True)
        return all_posts
