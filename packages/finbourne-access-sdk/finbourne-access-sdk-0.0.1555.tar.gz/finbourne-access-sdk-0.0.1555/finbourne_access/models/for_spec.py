# coding: utf-8

"""
    FINBOURNE Access Management API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.0.1555
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from finbourne_access.configuration import Configuration


class ForSpec(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'as_at_range_for_spec': 'AsAtRangeForSpec',
        'as_at_relative': 'AsAtRelative',
        'effective_date_has_quality': 'EffectiveDateHasQuality',
        'effective_date_relative': 'EffectiveDateRelative',
        'effective_range': 'EffectiveRange'
    }

    attribute_map = {
        'as_at_range_for_spec': 'asAtRangeForSpec',
        'as_at_relative': 'asAtRelative',
        'effective_date_has_quality': 'effectiveDateHasQuality',
        'effective_date_relative': 'effectiveDateRelative',
        'effective_range': 'effectiveRange'
    }

    required_map = {
        'as_at_range_for_spec': 'optional',
        'as_at_relative': 'optional',
        'effective_date_has_quality': 'optional',
        'effective_date_relative': 'optional',
        'effective_range': 'optional'
    }

    def __init__(self, as_at_range_for_spec=None, as_at_relative=None, effective_date_has_quality=None, effective_date_relative=None, effective_range=None, local_vars_configuration=None):  # noqa: E501
        """ForSpec - a model defined in OpenAPI"
        
        :param as_at_range_for_spec: 
        :type as_at_range_for_spec: finbourne_access.AsAtRangeForSpec
        :param as_at_relative: 
        :type as_at_relative: finbourne_access.AsAtRelative
        :param effective_date_has_quality: 
        :type effective_date_has_quality: finbourne_access.EffectiveDateHasQuality
        :param effective_date_relative: 
        :type effective_date_relative: finbourne_access.EffectiveDateRelative
        :param effective_range: 
        :type effective_range: finbourne_access.EffectiveRange

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._as_at_range_for_spec = None
        self._as_at_relative = None
        self._effective_date_has_quality = None
        self._effective_date_relative = None
        self._effective_range = None
        self.discriminator = None

        if as_at_range_for_spec is not None:
            self.as_at_range_for_spec = as_at_range_for_spec
        if as_at_relative is not None:
            self.as_at_relative = as_at_relative
        if effective_date_has_quality is not None:
            self.effective_date_has_quality = effective_date_has_quality
        if effective_date_relative is not None:
            self.effective_date_relative = effective_date_relative
        if effective_range is not None:
            self.effective_range = effective_range

    @property
    def as_at_range_for_spec(self):
        """Gets the as_at_range_for_spec of this ForSpec.  # noqa: E501


        :return: The as_at_range_for_spec of this ForSpec.  # noqa: E501
        :rtype: finbourne_access.AsAtRangeForSpec
        """
        return self._as_at_range_for_spec

    @as_at_range_for_spec.setter
    def as_at_range_for_spec(self, as_at_range_for_spec):
        """Sets the as_at_range_for_spec of this ForSpec.


        :param as_at_range_for_spec: The as_at_range_for_spec of this ForSpec.  # noqa: E501
        :type as_at_range_for_spec: finbourne_access.AsAtRangeForSpec
        """

        self._as_at_range_for_spec = as_at_range_for_spec

    @property
    def as_at_relative(self):
        """Gets the as_at_relative of this ForSpec.  # noqa: E501


        :return: The as_at_relative of this ForSpec.  # noqa: E501
        :rtype: finbourne_access.AsAtRelative
        """
        return self._as_at_relative

    @as_at_relative.setter
    def as_at_relative(self, as_at_relative):
        """Sets the as_at_relative of this ForSpec.


        :param as_at_relative: The as_at_relative of this ForSpec.  # noqa: E501
        :type as_at_relative: finbourne_access.AsAtRelative
        """

        self._as_at_relative = as_at_relative

    @property
    def effective_date_has_quality(self):
        """Gets the effective_date_has_quality of this ForSpec.  # noqa: E501


        :return: The effective_date_has_quality of this ForSpec.  # noqa: E501
        :rtype: finbourne_access.EffectiveDateHasQuality
        """
        return self._effective_date_has_quality

    @effective_date_has_quality.setter
    def effective_date_has_quality(self, effective_date_has_quality):
        """Sets the effective_date_has_quality of this ForSpec.


        :param effective_date_has_quality: The effective_date_has_quality of this ForSpec.  # noqa: E501
        :type effective_date_has_quality: finbourne_access.EffectiveDateHasQuality
        """

        self._effective_date_has_quality = effective_date_has_quality

    @property
    def effective_date_relative(self):
        """Gets the effective_date_relative of this ForSpec.  # noqa: E501


        :return: The effective_date_relative of this ForSpec.  # noqa: E501
        :rtype: finbourne_access.EffectiveDateRelative
        """
        return self._effective_date_relative

    @effective_date_relative.setter
    def effective_date_relative(self, effective_date_relative):
        """Sets the effective_date_relative of this ForSpec.


        :param effective_date_relative: The effective_date_relative of this ForSpec.  # noqa: E501
        :type effective_date_relative: finbourne_access.EffectiveDateRelative
        """

        self._effective_date_relative = effective_date_relative

    @property
    def effective_range(self):
        """Gets the effective_range of this ForSpec.  # noqa: E501


        :return: The effective_range of this ForSpec.  # noqa: E501
        :rtype: finbourne_access.EffectiveRange
        """
        return self._effective_range

    @effective_range.setter
    def effective_range(self, effective_range):
        """Sets the effective_range of this ForSpec.


        :param effective_range: The effective_range of this ForSpec.  # noqa: E501
        :type effective_range: finbourne_access.EffectiveRange
        """

        self._effective_range = effective_range

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ForSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ForSpec):
            return True

        return self.to_dict() != other.to_dict()
