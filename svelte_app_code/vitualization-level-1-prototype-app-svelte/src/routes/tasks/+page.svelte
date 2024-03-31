<script lang="ts">
    interface Task {
        id: number;
        title: string;
        completed: boolean;
    }

    let tasks: Task[] = [
        { id: 1, title: 'Task 1', completed: false },
        { id: 2, title: 'Task 2', completed: true },
        { id: 3, title: 'Task 3', completed: false }
    ];
</script>

<h1>Task List</h1>

<ul>
    {#each tasks as task (task.id)}
        <li>{task.title} - {task.completed ? 'Completed' : 'Incomplete'}</li>
    {/each}
</ul>