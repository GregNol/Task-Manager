import asyncio
from services import db
from config import config
from core import domain


async def main():
    # create async session maker (create_db_pool is async)
    session_maker = await db.create_db_pool(config.db_uri.get_secret_value())

    async with session_maker() as session:
        task_manager = db.TaskManager(session)

        # 1) list all tasks (should be empty initially)
        tasks = await task_manager.get_tasks()
        print("Initial tasks:", tasks)

        # 2) create a new task
        new_task = domain.Task(
            title="Sample Task",
            description="This is a sample task.",
            status=domain.Status.TODO
        )
        created = await task_manager.add_task(new_task)
        print(f"Created task id={created.id}, status={created.status}")

        # 3) get all tasks again
        tasks = await task_manager.get_tasks()
        print("Tasks after create:", tasks)

        # 4) get single task by id
        fetched = await task_manager.task(created.id)
        print("Fetched task:", fetched)

        # 5) update the task
        updated = await task_manager.update_task(created.id, title="Updated title")
        print("Updated task:", updated)

        # 6) filter tasks by status
        filtered = await task_manager.get_tasks(status=domain.Status.TODO)
        print("Filtered tasks (status=TODO):", filtered)

        # 7) delete the task
        deleted = await task_manager.del_task(created.id)
        print("Deleted task:", deleted)

        # 8) final list
        final = await task_manager.get_tasks()
        print("Final tasks:", final)


if __name__ == '__main__':
    asyncio.run(main())