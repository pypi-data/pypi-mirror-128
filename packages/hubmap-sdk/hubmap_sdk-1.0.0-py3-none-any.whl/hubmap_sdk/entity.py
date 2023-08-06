class Entity:

    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])
        # if dictionary['created_timestamp'] is not None:
        #     self.created_timestamp = dictionary['created_timestamp']
        # if dictionary['created_by_user_displayname'] is not None:
        #     self.created_by_user_displayname = dictionary['created_by_user_displayname']
        # if dictionary['created_by_user_email'] is not None:
        #     self.created_by_user_email = dictionary['created_by_user_email']
        # if dictionary['created_by_user_sub'] is not None:
        #     self.created_by_user_sub = dictionary['created_by_user_sub']
        # if dictionary['uuid'] is not None:
        #     self.uuid = dictionary['uuid']
        # if dictionary['hubmap_id'] is not None:
        #     self.hubmap_id = dictionary['hubmap_id']
        # if dictionary['last_modified_user_timestamp'] is not None:
        #     self.last_modified_user_timestamp = dictionary['last_modified_user_timestamp']
        # if dictionary['last_modified_user_sub'] is not None:
        #     self.last_modified_user_sub = dictionary['last_modified_user_sub']
        # if dictionary['last_modified_user_displayname'] is not None:
        #     self.last_modified_user_displayname = dictionary['last_modified_user_displayname']
        # if dictionary['last_modified_user_email'] is not None:
        #     self.last_modified_user_email = dictionary['last_modified_user_email']
        # if dictionary['entity_type'] is not None:
        #     self.entity_type = dictionary['entity_type']

    def get_uuid(self):
        return self.uuid
