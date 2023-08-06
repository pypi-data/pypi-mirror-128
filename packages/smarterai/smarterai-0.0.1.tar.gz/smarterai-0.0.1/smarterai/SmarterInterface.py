import inspect
from typing import Callable, Optional
from abc import ABCMeta, abstractmethod


class SmarterMessage(dict):
    pass


SmarterSender = Callable[[SmarterMessage, str], SmarterMessage]


class _Smarter_SignatureCheckerMeta(ABCMeta):
    def __init__(cls, name, bases, attrs):
        errors = []
        for base_class in bases:
            for func_name in getattr(base_class, "__abstractmethods__", ()):
                smarter_signature = inspect.getfullargspec(
                    getattr(base_class, func_name)
                )
                artifact_signature = inspect.getfullargspec(
                    getattr(cls, func_name)
                )
                if smarter_signature != artifact_signature:
                    errors.append(
                        "Abstract method {0} not implemented with "
                        "correct signature in {1}. Expected {2}.".format(
                            func_name, cls.__name__, smarter_signature
                        )
                    )
        if errors:
            raise TypeError("\n".join(errors))
        super().__init__(name, bases, attrs)


class SmarterPlugin(metaclass=_Smarter_SignatureCheckerMeta):
    """
    SmarterPlugin is designed for easy communication between the smarter.ai's platform and other artifacts.
    In order to have the artifact's code accessible to the platform, this class needs to be inherited from
    a class explicitly named SmarterArtifact.
    Example:
        Class SmarterArtifact(SmarterPlugin):
            pass
    """

    @abstractmethod
    def invoke(
        self, port: str, msg: SmarterMessage, send_message: SmarterSender
    ) -> Optional[SmarterMessage]:
        """
        This is the Artifact's messages entry point. Any message sent to the artifact will be routed to this method.
        This method needs to be overwritten.

        Example:
            Class SmarterArtifact(SmarterPlugin):
                def invoke(self, port: str,
                           msg: SmarterMessage,
                           send_message: SmarterSender) -> Optional[SmarterMessage]:
                    pass
        The message received and its associated port will be passed as inputs for this method,
        Along with a callable function that can be used to send messages to other artifacts.

        Arguments:
            port [str]: The input port name used to receive the message.
            msg [SmarterMessage]: The message passed to the artifact.
            send_message[SmarterSender]: A Callable function used to send messages to other artifacts.
                                        The function has the signature:
                                            Callable[[SmarterMessage, str], SmarterMessage]
                                        Example:
                                            send_message(SmarterMessage(), 'out_port_name')

                                        Arguments:
                                            [SmarterMessage]: The new message to send out.
                                            [str]: The output port name used to send the new message.

                                        Returns:
                                            [SmarterMessage]: A return message.

        Returns:
            Optional[SmarterMessage]: If a message is being returned it should be of
                                      type SmarterMessage or None
        """
        raise NotImplementedError
