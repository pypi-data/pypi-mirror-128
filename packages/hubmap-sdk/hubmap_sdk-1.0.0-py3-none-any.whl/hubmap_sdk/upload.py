from hubmap_sdk.entity import Entity


class Upload(Entity):
    def __init__(self, instance):
        super().__init__(instance)
        for key in instance:
            setattr(self, key, instance[key])
        # if instance['description'] is not None:
        #     self.description = instance['description']
        # if instance['title'] is not None:
        #     self.title = instance['title']
        # if instance['status'] is not None:
        #     self.status = instance['status']
        # if instance['validation_message'] is not None:
        #     self.validation_message = instance['validation_message']
        # if instance['group_uuid'] is not None:
        #     self.group_uuid = instance['group_uuid']
        # if instance['group_name'] is not None:
        #     self.group_name = instance['group_name']
        # if instance['datasets'] is not None:
        #     self.dataset = instance['datasets']
        # if instance['dataset_uuids_to_link'] is not None:
        #     self.dataset_uuids_to_link = instance['dataset_uuids_to_link']
        # if instance['dataset_uuids_to_unlink'] is not None:
        #     self.dataset_uuids_to_unlink = instance['dataset_uuids_to_unlink']
