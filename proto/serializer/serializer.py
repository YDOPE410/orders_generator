import abc


class Serializer(abc.ABC):

	@abc.abstractmethod
	def serialize(self, *args):
		pass