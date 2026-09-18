def test_get_tasks_without_authentication(client):
    response = client.get("/tasks")

    assert response.status_code == 401


def test_create_task(auth_client, authenticated_user):
    response = auth_client.post(
        "/tasks",
        json={
            "title": "Learn FastAPI Testing",
            "description": "Write authenticated API tests",
            "is_completed": False,
            "priority": "high",
            "due_date": None
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn FastAPI Testing"
    assert data["description"] == "Write authenticated API tests"
    assert data["is_completed"] is False
    assert data["priority"] == "high"
    assert data["user_id"] == authenticated_user["id"]


def test_get_tasks(auth_client, authenticated_user):
    # Create a task first because every test starts
    # with a fresh test database.
    create_response = auth_client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Task for get tasks test",
            "is_completed": False,
            "priority": "medium",
            "due_date": None
        }
    )

    assert create_response.status_code == 201

    # Get tasks
    response = auth_client.get("/tasks")

    assert response.status_code == 200

    data = response.json()

    assert "tasks" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data

    assert data["total"] >= 1
    assert len(data["tasks"]) >= 1

    # Verify every returned task belongs to the authenticated user
    for task in data["tasks"]:
        assert task["user_id"] == authenticated_user["id"]


def test_get_one_task(auth_client, authenticated_user):
    # Create a task first
    create_response = auth_client.post(
        "/tasks",
        json={
            "title": "Task for GET test",
            "description": "Testing get one task",
            "is_completed": False,
            "priority": "medium",
            "due_date": None
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # Get the specific task
    response = auth_client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Task for GET test"
    assert data["user_id"] == authenticated_user["id"]


def test_user_cannot_access_another_users_task(
    auth_client,
    second_auth_client,
):
    # User 1 creates a task
    create_response = auth_client.post(
        "/tasks",
        json={
            "title": "Private User 1 Task",
            "description": "This task belongs to another user",
            "is_completed": False,
            "priority": "high",
            "due_date": None
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # User 2 tries to access User 1's task
    response = second_auth_client.get(
        f"/tasks/{task_id}"
    )

    assert response.status_code == 404


def test_update_task(auth_client, authenticated_user):
    # Create task
    create_response = auth_client.post(
        "/tasks",
        json={
            "title": "Task Before Update",
            "description": "Original description",
            "is_completed": False,
            "priority": "medium",
            "due_date": None
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # Update task
    update_response = auth_client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Task After Update",
            "description": "Updated description",
            "is_completed": True,
            "priority": "high"
        }
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == task_id
    assert data["title"] == "Task After Update"
    assert data["description"] == "Updated description"
    assert data["is_completed"] is True
    assert data["priority"] == "high"
    assert data["user_id"] == authenticated_user["id"]


def test_delete_task(auth_client):
    # Create task
    create_response = auth_client.post(
        "/tasks",
        json={
            "title": "Task for Delete Test",
            "description": "This task will be deleted",
            "is_completed": False,
            "priority": "low",
            "due_date": None
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # Delete task
    delete_response = auth_client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 204

    # Verify task no longer exists
    get_response = auth_client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404


def test_create_task_without_authentication(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Unauthorized Task",
            "description": "This should not be created",
            "is_completed": False,
            "priority": "medium",
            "due_date": None
        }
    )

    assert response.status_code == 401


def test_create_task_with_invalid_title(auth_client):
    response = auth_client.post(
        "/tasks",
        json={
            "title": "",
            "description": "This should fail validation",
            "is_completed": False,
            "priority": "medium",
            "due_date": None
        }
    )

    assert response.status_code == 422


def test_create_task_with_invalid_priority(auth_client):
    response = auth_client.post(
        "/tasks",
        json={
            "title": "Invalid Priority Task",
            "description": "This should fail validation",
            "is_completed": False,
            "priority": "urgent",
            "due_date": None
        }
    )

    assert response.status_code == 422


def test_get_tasks_with_invalid_limit(auth_client):
    # limit = 0 should fail
    response = auth_client.get("/tasks?limit=0")

    assert response.status_code == 422

    # limit = 101 should fail
    response = auth_client.get("/tasks?limit=101")

    assert response.status_code == 422


def test_get_tasks_by_priority(auth_client, authenticated_user):
    # Create a HIGH priority task
    create_response = auth_client.post(
        "/tasks",
        json={
            "title": "High Priority Test",
            "description": "Testing priority filter",
            "is_completed": False,
            "priority": "high",
            "due_date": None
        }
    )

    assert create_response.status_code == 201

    # Get only HIGH priority tasks
    response = auth_client.get("/tasks?priority=high")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] >= 1

    for task in data["tasks"]:
        assert task["priority"] == "high"
        assert task["user_id"] == authenticated_user["id"]


def test_get_tasks_by_completion_status(auth_client, authenticated_user):
    # Create a completed task
    create_response = auth_client.post(
        "/tasks",
        json={
            "title": "Completed Task Test",
            "description": "Testing completed filter",
            "is_completed": True,
            "priority": "medium",
            "due_date": None
        }
    )

    assert create_response.status_code == 201

    # Get only completed tasks
    response = auth_client.get("/tasks?is_completed=true")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] >= 1

    for task in data["tasks"]:
        assert task["is_completed"] is True
        assert task["user_id"] == authenticated_user["id"]


def test_search_tasks(auth_client, authenticated_user):
    # Create a task with a unique title
    create_response = auth_client.post(
        "/tasks",
        json={
            "title": "FastAPI Search Testing",
            "description": "Testing task search functionality",
            "is_completed": False,
            "priority": "medium",
            "due_date": None
        }
    )

    assert create_response.status_code == 201

    # Search using part of the title
    response = auth_client.get("/tasks?search=Search")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] >= 1

    found = False

    for task in data["tasks"]:
        assert task["user_id"] == authenticated_user["id"]

        if task["title"] == "FastAPI Search Testing":
            found = True

    assert found is True


def test_sort_tasks_by_title_ascending(auth_client):
    # Create two tasks
    response_1 = auth_client.post(
        "/tasks",
        json={
            "title": "AAA Sorting Test",
            "description": "Sorting test A",
            "is_completed": False,
            "priority": "medium",
            "due_date": None
        }
    )

    response_2 = auth_client.post(
        "/tasks",
        json={
            "title": "ZZZ Sorting Test",
            "description": "Sorting test Z",
            "is_completed": False,
            "priority": "medium",
            "due_date": None
        }
    )

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    # Get tasks sorted by title ASC
    response = auth_client.get(
        "/tasks?sort_by=title&sort_order=asc"
    )

    assert response.status_code == 200

    data = response.json()

    titles = [task["title"] for task in data["tasks"]]

    assert titles == sorted(titles)


def test_task_pagination(auth_client):
    # Create two tasks
    response_1 = auth_client.post(
        "/tasks",
        json={
            "title": "Pagination Test 1",
            "description": "Testing pagination",
            "is_completed": False,
            "priority": "low",
            "due_date": None
        }
    )

    response_2 = auth_client.post(
        "/tasks",
        json={
            "title": "Pagination Test 2",
            "description": "Testing pagination",
            "is_completed": False,
            "priority": "low",
            "due_date": None
        }
    )

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    # First page
    response = auth_client.get(
        "/tasks?skip=0&limit=1"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["skip"] == 0
    assert data["limit"] == 1
    assert len(data["tasks"]) == 1
    assert data["has_previous"] is False
    assert data["has_next"] is True


def test_task_pagination_second_page(auth_client):
    # Create two tasks because every test starts
    # with a fresh test database.
    for i in range(2):
        response = auth_client.post(
            "/tasks",
            json={
                "title": f"Pagination Task {i + 1}",
                "description": f"Pagination test task {i + 1}",
                "is_completed": False,
                "priority": "medium",
                "due_date": None
            }
        )

        assert response.status_code == 201

    # Get second page
    response = auth_client.get(
        "/tasks?skip=1&limit=1"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 2
    assert data["skip"] == 1
    assert data["limit"] == 1
    assert len(data["tasks"]) == 1
    assert data["has_previous"] is True

