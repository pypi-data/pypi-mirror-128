import types


def attrs_filter(frame: types.FrameType, event: str, arg: object) -> bool:
    """
    Ignore attrs generated code

    The attrs library constructs an artificial filename for generated
    class methods like __init__ and __hash__.
    """
    return frame.f_code.co_filename.startswith("<attrs generated")
