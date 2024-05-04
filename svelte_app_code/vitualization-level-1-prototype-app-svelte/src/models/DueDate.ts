/**
 * Represents a due date for a Task.
 */
export interface DueDate {
    /**
     * The ID of the Task.
     */
    task_id: number;
    
    /**
     * The due date.
     */
    due_date: Date;
    
    /**
     * Indicates whether the due date is active.
     */
    is_active: boolean;
}