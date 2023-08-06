# Authorizer

## Описание

Утилитарный пакет, содержащий в себе интеграционный модуль с сервисом Authorizer.

## Установка библиотеки

```
pip install vtb-authorizer-utils
```

с инструментами тестирования и проверки качества кода

```
pip install vtb-authorizer-utils[test]
```

## Быстрый старт

### AuthorizerGateway

Создание объекта AuthorizerGateway от имени сервисной учетной записи. Некоторые сервисы требуют вызов от имени учетной
записи портала.

```python
from dotenv import load_dotenv
from envparse import env
from vtb_authorizer_utils.gateway import AuthorizerGateway
from vtb_http_interaction.http_utils import make_environ_keycloak_config

load_dotenv()

keycloak_config = make_environ_keycloak_config()

authorizer_base_url = env.str('AUTHORIZER_BASE_URL')
redis_url = env.str('REDIS_URL')

gateway = AuthorizerGateway(authorizer_base_url, keycloak_config, redis_url)
```

Создание объекта AuthorizerGateway от имени учетной записи портала (требуется access_token от keycloak)

```python
from dotenv import load_dotenv
from envparse import env
from vtb_authorizer_utils.gateway import AuthorizerGateway
from vtb_http_interaction.keycloak_gateway import KeycloakGateway, UserCredentials
from vtb_http_interaction.http_utils import make_environ_keycloak_config

load_dotenv()

keycloak_config = make_environ_keycloak_config()

user_credentials = UserCredentials(
    username=env.str('KEYCLOAK_TEST_USER_NAME'),
    password=env.str('KEYCLOAK_TEST_USER_PASSWORD')
)

authorizer_base_url = env.str('AUTHORIZER_BASE_URL')
redis_url = env.str('REDIS_URL')

with KeycloakGateway(keycloak_config) as gateway:
    gateway.obtain_token(user_credentials, grant_type=("password",))
    access_token = gateway.access_token

gateway = AuthorizerGateway(authorizer_base_url, access_token=access_token)
```

### Работа с организациями

Получение списка организаций

```
organizations = await gateway.get_organizations()
```

Получение организации по name

```
organization = await gateway.get_organization(name)
```

Получение проектов организации

```
projects = await user_gateway.get_organization_projects(name)
```

Получение потомков организации

```
children = await user_gateway.get_organization_children(name)
```

Получение структуры организации

```
children = await user_gateway.get_organization_structure(name)
```

### Работа с папками

Получение папки

```
folder = await user_gateway.get_folder(name)
```

Получение потомков папки

```
folder = await user_gateway.get_folder_children(name)
```

Получение предков папки

```
folder = await user_gateway.get_folder_ancestors(name)
```

### Работа с проектами

Получение проекта по name

```
project = await user_gateway.get_project(name)
```

Получение предков проекта

```
project = await user_gateway.get_project_ancestors(name)
```

### Работа с пользователями

Получение списка пользователей

```
users = await gateway.get_users(page=1, per_page=10, firstname="иванов", lastname="иванов")
```

Получение пользователя по его идентификатору

```
user = await gateway.get_user(users[0].remote_id)
```

### Прочее

Генерация полного пути объекта контекста в иерархии

```
full_structure_path = await generate_full_structure_path(gateway, Organization(name='vtb'))

full_structure_path = await generate_full_structure_path(gateway,
                                                             Folder(name='fold-qodfpmmu0q', organization='vtb'))
                                                             
full_structure_path = await generate_full_structure_path(gateway,
                                                             Project(name='proj-srv3y9v8m0', organization='vtb'))
```

Загрузка конфигурации ресурсных типов и правил для сервиса в виде словаря

```
with open(file, encoding="utf-8") as json_file:
    cfg = json.load(json_file)
    service, resource_types, resource_rules = await import_service_from_dict(gateway, cfg)
```

### Построение схемы импорта сервиса в Authorizer

Добавление информации о сервисе для импорта в Authorizer

```
authorizer_service(name='state-service',
                   title='Сервис состояний',
                   description='',
                   url=settings.KONG_STATE_SERVICE_URL)
```

Добавление информации о ресурсном типе для импорта в Authorizer

```
@authorizer_resource_type(service='state-service',
                          name='inventories',
                          title='Объекты инфраструктуры',
                          description='')
```

Добавление информации о ресурсном правиле для импорта в Authorizer

```
@authorizer_resource_rule(context_types={ContextType.ORGANIZATIONS, ContextType.FOLDERS, ContextType.PROJECTS},
                              http_method='POST',
                              url_pattern='/api/v1/tag-manager/{context_type}/{id}/inventories/',
                              access_type='members',
                              operation_name='Список объектов инфраструктуры')
```

В случае, если пометить класс декоратором authorizer_resource_type, указав у него base_url_pattern, автоматически будут
сгенерированы правила авторайзера для REST API по умолчанию:

1. для методов класса get, post, put, patch, delete, create, retrieve, update, list, destroy
2. для методов, помеченных декоратором django `@action`

```
@authorizer_resource_type(service='tags-service', name='tags', title='Теги', description='',
                          base_url_pattern='/api/v1/{context_type}/{id}/tags/',
                          default_context_types=ALL_CONTEXT_TYPES)
```