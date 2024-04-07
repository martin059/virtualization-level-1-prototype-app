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
     * The creation date of the task.
     */
    creation_date: Date;

    /**
     * The status of the task.
     * Possible values: 'Created', 'Done', 'Deleted', 'Dropped', 'Postponed'.
     */
    task_status: 'Created' | 'Done' | 'Deleted' | 'Dropped' | 'Postponed';
}