from hubmap_sdk.entity import Entity


class Dataset(Entity):
    def __init__(self, instance):
        super().__init__(instance)
        for key in instance:
            setattr(self, key, instance[key])
        # if ['registered_doi'] is not None:
        #     self.registered_doi = ['registered_doi']
        # if ['doi_url'] is not None:
        #     self.doi_url = ['doi_url']
        # if ['creators'] is not None:
        #     self.creators = ['creators']
        # if ['contacts'] is not None:
        #     self.contacts = ['contacts']
        # if ['antibodies'] is not None:
        #     self.antibodies = ['antibodies']
        # if ['description'] is not None:
        #     self.description = ['description']
        # if ['data_access_level'] is not None:
        #     self.data_access_level = ['data_access_level']
        # if ['contains_human_genetic_sequences'] is not None:
        #     self.contains_human_genetic_sequences = ['contains_human_genetic_sequences']
        # if ['status'] is not None:
        #     self.status = ['status']
        # if ['title'] is not None:
        #     self.title = ['title']
        # if ['data_types'] is not None:
        #     self.data_types = ['data_types']
        # if ['upload'] is not None:
        #     self.upload = ['upload']
        # if ['collections'] is not None:
        #     self.collections = ['collections']
        # if ['contributors'] is not None:
        #     self.contributors = ['contributors']
        # if ['direct_ancestors'] is not None:
        #     self.direct_ancestors = ['direct_ancestors']
        # if ['published_timestamp'] is not None:
        #     self.published_timestamp = ['published_timestamp']
        # if ['published_user_displayname'] is not None:
        #     self.published_user_displayname = ['published_user_displayname']
        # if ['published_user_sub'] is not None:
        #     self.published_user_sub = ['published_user_sub']
        # if ['published_user_email'] is not None:
        #     self.published_user_email = ['published_user_email']
        # if ['ingest_metadata'] is not None:
        #     self.ingest_metadata = ['ingest_metadata']
        # if ['local_directory_rel_path'] is not None:
        #     self.local_directory_rel_path = ['local_directory_rel_path']
        # if ['group_uuid'] is not None:
        #     self.group_uuid = ['group_uuid']
        # if ['group_uuid'] is not None:
        #     self.group_name = ['group_name']
        # if ['previous_revision_uuid'] is not None:
        #     self.previous_revision_uuid = ['previous_revision_uuid']
        # if ['next_revision_uuid'] is not None:
        #     self.next_revision_uuid = ['next_revision_uuid']
        # if ['thumbnail_file'] is not None:
        #     self.thumbnail_file = ['thumbnail_file']
        # if ['thumbnail_file_to_add'] is not None:
        #     self.thumbnail_file_to_add = ['thumbnail_file_to_add']
        # if ['thumbnail_file_to_remove'] is not None:
        #     self.thumbnail_file_to_remove = ['thumbnail_file_to_remove']

