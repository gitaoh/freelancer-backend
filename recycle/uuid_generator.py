import uuid


class UUIDGenerator:
    model = None

    def generate_uuid(self):
        """Loop over model objects to ensure unique uuid"""
        generate = uuid.uuid4()
        try:
            self.model.objects.get(uuid__exact=generate)
        except self.model.DoesNotExist as e:
            return generate
        else:
            self.generate_uuid()
