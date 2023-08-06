from hubmap_sdk.entity import Entity


class Sample(Entity):
    def __init__(self, instance):
        super().__init__(instance)
        for key in instance:
            setattr(self, key, instance[key])
        # if instance['registered_doi'] is not None:
        #     self.registered_doi = instance['registered_doi']
        # if instance['doi_url'] is not None:
        #     self.doi_url = instance['doi_url']
        # if instance['creators'] is not None:
        #     self.creators = instance['creators']
        # if instance['contacts'] is not None:
        #     self.contacts = instance['contacts']
        # if instance['description'] is not None:
        #     self.description = instance['description']
        # if instance['data_access_level'] is not None:
        #     self.data_access_level = instance['data_access_level']
        # if instance['specimen_type'] is not None:
        #     self.specimen_type = instance['specimen_type']
        # if instance['specimen_type_other'] is not None:
        #     self.specimen_type_other = instance['specimen_type_other']
        # if instance['protocol_url'] is not None:
        #     self.protocol_url = instance['protocol_url']
        # if instance['group_uuid'] is not None:
        #     self.group_uuid = instance['group_uuid']
        # if instance['group_name'] is not None:
        #     self.group_name = instance['group_name']
        # if instance['organ'] is not None:
        #     self.organ = instance['organ']
        # if instance['organ_other'] is not None:
        #     self.organ_other = instance['organ_other']
        # if instance['direct_ancestor_uuid'] is not None:
        #     self.direct_ancestor_uuid = instance['direct_ancestor_uuid']
        # if instance['submission_id'] is not None:
        #     self.submission_id = instance['submission_id']
        # if instance['lab_tissue_sample_id'] is not None:
        #     self.lab_tissue_sample_id = instance['lab_tissue_sample_id']
        # if instance['rui_location'] is not None:
        #     self.rui_location = instance['rui_location']
        # if instance['metadata'] is not None:
        #     self.metadata = instance['metadata']
        # if instance['visit'] is not None:
        #     self.visit = instance['visit']
        # if instance['image_files'] is not None:
        #     self.image_files = instance['image_files']
        # if instance['image_files_to_add'] is not None:
        #     self.image_files_to_add = instance['image_files_to_add']
        # if instance['image_files_to_remove'] is not None:
        #     self.image_files_to_remove = instance['image_files_to_remove']
        # if instance['metadata_files'] is not None:
        #     self.metadata_files = instance['metadata_files']
        # if instance['metadata_files_to_add'] is not None:
        #     self.metadata_files_to_add = instance['metadata_files_to_add']
        # if instance['metadata_files_to_remove'] is not None:
        #     self.metadata_files_to_remove = instance['metadata_files_to_remove']
