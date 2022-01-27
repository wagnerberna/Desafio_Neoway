from http.cookiejar import MozillaCookieJar
import pytest
from pytest import fixture
from service.process_data import ProcessData


class TestProcessData:
    @fixture
    def my_setup(self, mocker):
        self.mocker = mocker
        self.mock_process_data = ProcessData()


class TestValidateCpf(TestProcessData):
    @pytest.mark.parametrize("cpf", ["06735742028", "77852171060", "21288948085"])
    def test_validate_cpf_successful(self, cpf, my_setup):
        response_expected = True
        response_result = self.mock_process_data.validate_cpf(cpf)
        assert response_expected == response_result

    @pytest.mark.parametrize("cpf", ["0", "1", "12345", "1234567890"])
    def test_validate_cpf_invalid_length(self, cpf, my_setup):
        response_expected = False
        response_result = self.mock_process_data.validate_cpf(cpf)
        assert response_expected == response_result

    @pytest.mark.parametrize("cpf", ["06735742025", "77852171050", "21288948070"])
    def test_validate_cpf_invalid_digit(self, cpf, my_setup):
        response_expected = False
        response_result = self.mock_process_data.validate_cpf(cpf)
        assert response_expected == response_result

    @pytest.mark.parametrize("cpf", (char * 11 for char in "1234567890"))
    def test_validate_cpf_error_repeated_number(self, cpf, my_setup):
        response_expected = False
        response_result = self.mock_process_data.validate_cpf(cpf)
        assert response_expected == response_result
