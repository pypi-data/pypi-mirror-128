from hubmap_sdk.entity import Entity


class Collection(Entity):
    def __init__(self, instance):
        super().__init__(instance)
        for key in instance:
            setattr(self, key, instance[key])
        # if instance['datasets'] is not None:
        #     self.datasets = instance['datasets']
        # if instance['registered_doi'] is not None:
        #     self.registered_doi = instance['registered_doi']
        # if instance['doi_url'] is not None:
        #     self.doi_url = instance['doi_url']
        # if instance['creators'] is not None:
        #     self.creators = instance['creators']
        # if instance['contacts'] is not None:
        #     self.contacts = instance['contacts']
        # if instance['title'] is not None:
        #     self.title = instance['title']