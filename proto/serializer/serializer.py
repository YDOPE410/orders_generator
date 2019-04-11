import abc


class Serializer(abc.ABC):

	@abc.abstractmethod
	def serialize(self, *args):
		pass

	@abc.abstractmethod
	def deserialize(self, *args):
		pass