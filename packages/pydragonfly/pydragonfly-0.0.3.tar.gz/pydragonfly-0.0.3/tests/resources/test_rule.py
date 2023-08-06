from . import APIResourceBaseTestCase, APIResource

from tests.mock_utils import generic_200_mock, generic_201_mock


class RuleResourceTestCase(APIResourceBaseTestCase):
    @property
    def resource(self) -> APIResource:
        return self.df.Rule

    @generic_201_mock
    def test__create(self, *args, **kwargs):
        response = self.resource.create(
            data=self.resource.CreateRuleRequestBody(
                rule="testrule",
                weight=0,
                variables=["x", "y"],
                modules={
                    "and": [{"module": "Api", "syscall": "VirtualAlloc"}],
                    "order": True,
                },
                malware_family="test__create",
                malware_behaviour="PUA",
                sensitive=False,
                meta_description={"author": "test__create"},
            )
        )
        self.assertEqual(201, response.code)

    @generic_200_mock
    def test__update(self, *args, **kwargs):
        response = self.resource.update(
            object_id=self.object_id,
            data=self.resource.UpdateRuleRequestBody(enabled=False),
        )
        self.assertEqual(200, response.code)

    @generic_200_mock
    def test__aggregate_malware_behaviour(self, *args, **kwargs):
        response = self.resource.aggregate_malware_behaviour()
        self.assertEqual(200, response.code)
