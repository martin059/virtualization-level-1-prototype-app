/**
 * Represents a task.
 */
export interface Task {
    /**
     * The unique identifier of the task.
     */
    id: number;

    /**
     * The name of the task.
     */
    task_name: string;

    /**
     * The description of the task.
     */
    task_descrip: string;

    /**
     * The creation date of the task. With format 'YYYY-MM-DD'.
     */
    creation_date: string;

    /**
     * Optional date that represents the due_date of the task. With format 'YYYY-MM-DD'.
     * Used solely for creating a task with an initial due date. 
     * With the app current design, a given task can have multiple due dates but only one can be "active" at a time.
     */
    due_date?: string;

    /**
     * The status of the task.
     * Possible values: 'Created', 'Done', 'Deleted', 'Dropped', 'Postponed'.
     */
    task_status: 'Created' | 'Done' | 'Deleted' | 'Dropped' | 'Postponed';
}