import os
import uuid
from dataclasses import dataclass
from unittest.mock import MagicMock

import django
import pytest
from celery import current_app
from django.conf import settings

# Configure Django settings for testing
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EditEngine.settings")
if not settings.configured:
    django.setup()

from data.models.edit_task import EditTask
from services.tasks.edit_tasks import process_edit_task


@dataclass
class ParagraphResult:
    before: str
    after: str
    status: str


@pytest.fixture(autouse=True)
def celery_eager():
    # Run Celery tasks synchronously for testing
    current_app.conf.task_always_eager = True
    yield
    current_app.conf.task_always_eager = False






@pytest.mark.django_db
def test_process_edit_task_article_section(monkeypatch):
    # Create a test EditTask
    edit_task = EditTask.objects.create(
        editing_mode="brevity",
        article_title="Test",
        section_title="Intro",
        llm_provider="google",
    )

    async def mock_edit_article_section_structured(
        article_title, section_title, language="en", progress_callback=None
    ):
        return [ParagraphResult(before="baz", after="qux", status="CHANGED")]

    mock_editor = MagicMock()
    mock_editor.edit_article_section_structured = mock_edit_article_section_structured
    monkeypatch.setattr(
        "services.tasks.edit_tasks.WikiEditor", lambda **kwargs: mock_editor
    )
    monkeypatch.setattr(
        "services.tasks.edit_tasks._initialize_llm", lambda config: MagicMock()
    )
    result = process_edit_task(
        editing_mode="brevity",
        llm_config={"provider": "google"},
        edit_task_id=str(edit_task.id),
        article_title="Test",
        section_title="Intro",
    )
    assert isinstance(result, dict)
    assert "paragraphs" in result
    assert result["paragraphs"][0]["after"] == "qux"
    assert result["article_title"] == "Test"
    assert result["section_title"] == "Intro"
    assert result["article_url"].endswith("/Test")

    # Verify the EditTask was updated
    edit_task.refresh_from_db()
    assert edit_task.status == "SUCCESS"
    assert edit_task.result["paragraphs"][0]["after"] == "qux"


@pytest.mark.django_db
def test_process_edit_task_handles_exception(monkeypatch):
    # Create a test EditTask
    edit_task = EditTask.objects.create(
        editing_mode="copyedit",
        article_title="Test Article",
        section_title="Test Section",
        llm_provider="openai"
    )

    mock_editor = MagicMock()
    mock_editor.edit_article_section_structured.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "services.tasks.edit_tasks.WikiEditor", lambda **kwargs: mock_editor
    )
    monkeypatch.setattr(
        "services.tasks.edit_tasks._initialize_llm", lambda config: MagicMock()
    )
    result = process_edit_task(
        editing_mode="copyedit",
        llm_config={"provider": "openai"},
        edit_task_id=str(edit_task.id),
        article_title="Test Article",
        section_title="Test Section",
    )
    assert isinstance(result, dict)
    assert "error" in result
    assert "An unexpected error occurred. Please try again." in result["error"]

    # Verify the EditTask was marked as failed
    edit_task.refresh_from_db()
    assert edit_task.status == "FAILURE"
    assert "An unexpected error occurred. Please try again." in edit_task.error_message


def test_initialize_llm_google(monkeypatch):
    from services.tasks.edit_tasks import _initialize_llm

    class DummyLLM:
        pass

    monkeypatch.setattr(
        "services.tasks.edit_tasks.ChatGoogleGenerativeAI", lambda **kwargs: DummyLLM()
    )
    config = {"provider": "google", "api_key": "fake"}
    llm = _initialize_llm(config)
    assert isinstance(llm, DummyLLM)


def test_initialize_llm_openai(monkeypatch):
    from services.tasks.edit_tasks import _initialize_llm

    class DummyLLM:
        pass

    monkeypatch.setattr(
        "services.tasks.edit_tasks.ChatOpenAI", lambda **kwargs: DummyLLM()
    )
    config = {"provider": "openai", "api_key": "fake"}
    llm = _initialize_llm(config)
    assert isinstance(llm, DummyLLM)


def test_initialize_llm_anthropic(monkeypatch):
    from services.tasks.edit_tasks import _initialize_llm

    class DummyLLM:
        pass

    monkeypatch.setattr(
        "services.tasks.edit_tasks.ChatAnthropic", lambda **kwargs: DummyLLM()
    )
    config = {"provider": "anthropic", "api_key": "fake"}
    llm = _initialize_llm(config)
    assert isinstance(llm, DummyLLM)


def test_initialize_llm_mistral(monkeypatch):
    from services.tasks.edit_tasks import _initialize_llm

    class DummyLLM:
        pass

    monkeypatch.setattr(
        "services.tasks.edit_tasks.ChatMistralAI", lambda **kwargs: DummyLLM()
    )
    config = {"provider": "mistral", "api_key": "fake"}
    llm = _initialize_llm(config)
    assert isinstance(llm, DummyLLM)


def test_initialize_llm_perplexity(monkeypatch):
    from services.tasks.edit_tasks import _initialize_llm

    class DummyLLM:
        pass

    monkeypatch.setattr(
        "services.tasks.edit_tasks.ChatPerplexity", lambda **kwargs: DummyLLM()
    )
    config = {"provider": "perplexity", "api_key": "fake"}
    llm = _initialize_llm(config)
    assert isinstance(llm, DummyLLM)


def test_initialize_llm_invalid():
    from api.exceptions.user_facing_exceptions import ValidationError
    from services.tasks.edit_tasks import _initialize_llm

    config = {"provider": "invalid", "api_key": "fake"}
    with pytest.raises(ValidationError, match="Invalid LLM provider specified"):
        _initialize_llm(config)


@pytest.mark.django_db
def test_process_edit_task_value_error(monkeypatch):
    # Should return error dict if article_title or section_title is not str
    edit_task1 = EditTask.objects.create(editing_mode="brevity", llm_provider="google")
    edit_task2 = EditTask.objects.create(editing_mode="brevity", llm_provider="google")

    monkeypatch.setattr(
        "services.tasks.edit_tasks._initialize_llm", lambda config: MagicMock()
    )
    monkeypatch.setattr(
        "services.tasks.edit_tasks.WikiEditor", lambda **kwargs: MagicMock()
    )
    result1 = process_edit_task(
        editing_mode="brevity",
        llm_config={"provider": "google"},
        edit_task_id=str(edit_task1.id),
        article_title=None,
        section_title="Intro",
    )
    result2 = process_edit_task(
        editing_mode="brevity",
        llm_config={"provider": "google"},
        edit_task_id=str(edit_task2.id),
        article_title="Test",
        section_title=None,
    )
    assert (
        "error" in result1
        and "article_title and section_title must be provided as strings"
        in result1["error"]
    )
    assert (
        "error" in result2
        and "article_title and section_title must be provided as strings"
        in result2["error"]
    )

    # Verify the EditTasks were marked as failed
    edit_task1.refresh_from_db()
    edit_task2.refresh_from_db()
    assert edit_task1.status == "FAILURE"
    assert edit_task2.status == "FAILURE"


@pytest.mark.django_db
def test_process_edit_task_nonexistent_edit_task(monkeypatch):
    # Test with non-existent EditTask ID
    fake_uuid = str(uuid.uuid4())

    monkeypatch.setattr(
        "services.tasks.edit_tasks._initialize_llm", lambda config: MagicMock()
    )
    result = process_edit_task(
        editing_mode="copyedit",
        llm_config={"provider": "openai"},
        edit_task_id=fake_uuid,
        article_title="Test Article",
        section_title="Test Section",
    )

    assert isinstance(result, dict)
    assert "error" in result
    assert f"EditTask with id {fake_uuid} not found" in result["error"]


def test_run_async_safely_with_event_loop(monkeypatch):
    """Test _run_async_safely when an event loop is already running."""
    from services.tasks.edit_tasks import _run_async_safely

    # Create a mock coroutine object instead of a real one
    mock_coro = MagicMock()

    # Mock asyncio.get_running_loop to simulate running event loop
    def mock_get_running_loop():
        return MagicMock()  # Return a mock loop to simulate running loop

    monkeypatch.setattr("asyncio.get_running_loop", mock_get_running_loop)

    # Mock concurrent.futures to capture the call
    mock_executor = MagicMock()
    mock_future = MagicMock()
    mock_future.result.return_value = "test_result"
    mock_executor.submit.return_value = mock_future
    mock_executor.__enter__ = lambda self: self
    mock_executor.__exit__ = lambda self, *args: None

    mock_thread_pool = MagicMock(return_value=mock_executor)
    monkeypatch.setattr("concurrent.futures.ThreadPoolExecutor", mock_thread_pool)

    result = _run_async_safely(mock_coro)

    assert result == "test_result"
    mock_executor.submit.assert_called_once()
    mock_future.result.assert_called_once()
