"""Tests for heroes routes."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_seed.api.dependencies.services import get_heroes_service
from fastapi_seed.api.heroes import router
from fastapi_seed.models.hero import Hero, HeroCreate


@pytest.fixture
def app():
    """Create test app."""
    test_app = FastAPI()
    test_app.include_router(router)
    return test_app


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def sample_hero_create():
    """Sample hero create data."""
    return HeroCreate(name="Spider-Man", secret_name="Peter Parker", age=25)


@pytest.fixture
def sample_hero():
    """Sample hero data."""
    return Hero(id=1, name="Spider-Man", secret_name="Peter Parker", age=25)


class TestCreateHero:
    """Test create hero endpoint."""

    def test_create_hero_success(
        self, client, mocker, sample_hero_create, sample_hero
    ):
        """Test successful hero creation."""
        # Arrange
        mock_service = mocker.Mock()
        mock_service.create_hero.return_value = sample_hero
        mocker.patch.object(
            client.app,
            "dependency_overrides",
            {get_heroes_service: lambda: mock_service},
        )

        # Act
        response = client.post("/heroes/", json=sample_hero_create.model_dump())

        # Assert
        assert response.status_code == 200
        assert response.json() == sample_hero.model_dump()
        mock_service.create_hero.assert_called_once_with(sample_hero_create)

    def test_create_hero_invalid_data(self, client, mocker):
        """Test hero creation with invalid data."""
        # Arrange
        mock_service = mocker.Mock()
        mocker.patch.object(
            client.app,
            "dependency_overrides",
            {get_heroes_service: lambda: mock_service},
        )
        invalid_data = {"name": ""}  # Missing required fields

        # Act
        response = client.post("/heroes/", json=invalid_data)

        # Assert
        assert response.status_code == 422
        mock_service.create_hero.assert_not_called()

    def test_create_hero_service_error(
        self, client, mocker, sample_hero_create
    ):
        """Test hero creation when service raises an error."""
        # Arrange
        mock_service = mocker.Mock()
        mock_service.create_hero.side_effect = Exception("Database error")
        mocker.patch.object(
            client.app,
            "dependency_overrides",
            {get_heroes_service: lambda: mock_service},
        )

        # Act
        response = client.post("/heroes/", json=sample_hero_create.model_dump())

        # Assert
        assert response.status_code == 500
        mock_service.create_hero.assert_called_once_with(sample_hero_create)


class TestReadHeroes:
    """Test read heroes endpoint."""

    def test_read_heroes_success(self, client, mocker):
        """Test successful heroes retrieval."""
        # Arrange
        heroes = [
            Hero(id=1, name="Spider-Man", secret_name="Peter Parker", age=25),
            Hero(id=2, name="Iron Man", secret_name="Tony Stark", age=45),
        ]
        mock_service = mocker.Mock()
        mock_service.get_heroes.return_value = heroes
        mocker.patch.object(
            client.app,
            "dependency_overrides",
            {get_heroes_service: lambda: mock_service},
        )

        # Act
        response = client.get("/heroes/")

        # Assert
        assert response.status_code == 200
        assert response.json() == [hero.model_dump() for hero in heroes]
        mock_service.get_heroes.assert_called_once_with()

    def test_read_heroes_empty_list(self, client, mocker):
        """Test heroes retrieval when no heroes exist."""
        # Arrange
        mock_service = mocker.Mock()
        mock_service.get_heroes.return_value = []
        mocker.patch.object(
            client.app,
            "dependency_overrides",
            {get_heroes_service: lambda: mock_service},
        )

        # Act
        response = client.get("/heroes/")

        # Assert
        assert response.status_code == 200
        assert response.json() == []
        mock_service.get_heroes.assert_called_once_with()

    def test_read_heroes_service_error(self, client, mocker):
        """Test heroes retrieval when service raises an error."""
        # Arrange
        mock_service = mocker.Mock()
        mock_service.get_heroes.side_effect = Exception("Database error")
        mocker.patch.object(
            client.app,
            "dependency_overrides",
            {get_heroes_service: lambda: mock_service},
        )

        # Act
        response = client.get("/heroes/")

        # Assert
        assert response.status_code == 500
        mock_service.get_heroes.assert_called_once_with()


class TestRouterConfiguration:
    """Test router configuration."""

    def test_router_prefix(self):
        """Test router has correct prefix."""
        assert router.prefix == "/heroes"

    def test_router_tags(self):
        """Test router has correct tags."""
        assert router.tags == ["heroes"]
