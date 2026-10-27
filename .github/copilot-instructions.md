# Project Guidelines

## Code Style
- Prefer the existing Django and DRF style in this repository: small focused modules, explicit imports, and minimal changes that fit current naming and layering.
- Keep code consistent with the surrounding app structure under [apps/](../apps/). Use the shared helpers in [apps/common/](../apps/common/) instead of duplicating behavior.
- Use Spanish labels and text where the project already does so, especially in templates, forms, and model metadata.

## Architecture
- This is a Django REST Framework project with three main app areas: [apps/common/](../apps/common/), [apps/products_app/](../apps/products_app/), and [apps/users_app/](../apps/users_app/).
- Shared API infrastructure lives in [apps/common/models.py](../apps/common/models.py), [apps/common/views.py](../apps/common/views.py), [apps/common/serializers.py](../apps/common/serializers.py), and related helpers.
- Product-domain code is split into subpackages such as models, serializers, views, filters, services, tests, and management commands under [apps/products_app/](../apps/products_app/).
- Route and API wiring live in [project_site/urls.py](../project_site/urls.py) and project settings live in [project_site/settings.py](../project_site/settings.py).
- There is an existing backend-focused agent customization in [.github/agents/python-structure-optimizer.agent.md](agents/python-structure-optimizer.agent.md); reference it instead of duplicating its constraints here.

## Build and Test
- Set up a local environment with Python 3.11, then install dependencies from [requirements.txt](../requirements.txt).
- Run database migrations with `python manage.py migrate`.
- Start the development server with `python manage.py runserver`.
- Run tests with `pytest`; test discovery is configured by [pytest.ini](../pytest.ini).
- The API documentation is exposed at `/api/swagger/` when the server is running.

## Conventions
- Prefer adding or updating tests alongside backend changes, especially for new behavior in models, serializers, views, filters, and management commands.
- Preserve the existing separation between read and write concerns in serializers and viewsets when that pattern is already in use.
- Keep changes focused; avoid broad rewrites or new architectural patterns unless the current structure clearly needs them.
- Reuse existing shared pagination, permissions, and filtering helpers from [apps/common/](../apps/common/) instead of introducing parallel implementations.
- Treat [README.md](../README.md) as the source for local setup notes and existing project commands, and avoid copying that content here.