from common.db.session import Session
from common.db.models import TaskModel
from common.schemas.tasks import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(TaskModel).all()

    def get_by_id(self, task_id: int):
        return self.db.query(TaskModel).filter(TaskModel.id == task_id).first()

    def create(self, task: TaskCreate):
        db_task = TaskModel(**task.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def update(self, task_id: int, task_update: TaskUpdate):
        task = self.get_by_id(task_id)
        if not task:
            return None
        for field, value in task_update.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int):
        task = self.get_by_id(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
        return task