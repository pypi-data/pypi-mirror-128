import falcon
from typing import Dict, List, Any, Optional


class ApplicationError(falcon.HTTPError):

    def __init__(self, title: str = None, description: str = None, *args, **kwargs):
        super(ApplicationError, self).__init__(
            falcon.HTTP_400,
            title=title or getattr(
                self.__class__, 'name', None) or self.__class__.__name__.replace("Error", ""),
            description=description or getattr(
                self.__class__, 'description', None) or "Some error occured",
            *args,
            **kwargs
        )


class SchemaValidationError(ApplicationError):
    name = "SchemaValidationFailed"
    description = "One or more fields don't follow schema"

    def __init__(self, fields: Dict[str, Any], description: Optional[str] = None, code: Optional[str] = '200'):
        super(SchemaValidationError, self).__init__(
            title='SchemaValidationFailed',
            description=description,
            code=code
        )
        self.fields = fields

    def to_dict(self, obj_type=dict):
        result = super().to_dict(obj_type)
        result['fields'] = self.fields
        return result


class ObjectDoesntExistError(ApplicationError):
    name = "ObjectDoesntExist"
    description = "{object} for {parameter_type}({parameter_value}) doesn't exist"

    def __init__(self, object: str, parameter_type: str, parameter_value: str, *args, **kwargs):
        super(ObjectDoesntExistError, self).__init__(
            title=ObjectDoesntExistError.name,
            description=ObjectDoesntExistError.description.format(
                object=object, parameter_type=parameter_type, parameter_value=parameter_value),
            *args, **kwargs
        )


class InvalidParameterTypeError(ApplicationError):
    name = "InvalidParameterType"
    description = "{parameter_type} is not a valid parameter for {func_name}"

    def __init__(self, parameter_type: str, func_name: str, *args, **kwargs):
        super(InvalidParameterTypeError, self).__init__(
            title=InvalidParameterTypeError.name,
            description=InvalidParameterTypeError.description.format(
                parameter_type=parameter_type, func_name=func_name),
            *args, **kwargs
        )


class InvalidRequestParameterError(ApplicationError):
    name = "InvalidRequestParameter"
    description = "{parameter} is not a valid {parameter_type}"

    def __init__(self, parameter: str, parameter_type: str, *args, **kwargs):
        super(InvalidRequestParameterError, self).__init__(
            title=InvalidRequestParameterError.name,
            description=InvalidRequestParameterError.description.format(
                parameter=parameter, parameter_type=parameter_type),
            *args, **kwargs
        )


class UnAuthorizedSession(ApplicationError):
    name = "UnAuthorizedSession"
    description = "Request is not authenticated"
