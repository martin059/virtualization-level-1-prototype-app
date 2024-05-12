<script lang="ts">
// @ts-nocheck
  import { Col, NavBar, Button } from "@components/commonComponents";
  import { Notifications, acts } from '@tadashi/svelte-notification'
  import type { Task } from "@models/Task";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  // By default, the new task is created with the status 'Created'
  let newTask: Task = { task_name: '', task_descrip: '', task_status: 'Created', due_date: null };

  let submitEnabled: boolean;
  let goingBack: boolean = false;

  onMount(() => {
    submitEnabled = true;
  });

  async function handleSubmit() {
    if (goingBack) return; // if returning don't handle form
    if(isTaskNameValid()) {
      if (submitEnabled){
        submitEnabled = false;
        const res = await fetch('http://localhost:5001/tasks', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(newTask),
          timeout: 10000 // 10 seconds
        });
        const response = await res.json();
        const statusCode = res.status;
        if (statusCode >= 200 && statusCode < 300) {
          acts.add({ mode: 'success', message: 'Task created successfully. Redirecting to task page...', lifetime: 2});
          await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2 seconds so user can read message
          goto('/tasks');
        } else {
          acts.add({ mode: 'error', message: 'Something went wrong, for more info consult the console.' });
          console.log('Status response code: ' + statusCode + ';Response: ');
          console.log(response);
        }
        submitEnabled = true;
      } else {
        acts.add({ mode: 'warn', message: 'Wait until a response is returned.', lifetime: 3 });
      }
    }
  }

  function isTaskNameValid(): boolean {
    if (newTask.task_name.trim() === '') {
      acts.add({ mode: 'error', message: 'Task name must not be empty.', lifetime: 3 });
      return false;
    } else {
      return true;
    }
  }

  function goBack() {
    goingBack = true;
    goto('/tasks');
  }

</script>

<main class="d-flex flex-row full-height">
  <Col class="col-1">
    <NavBar />
  </Col>
  <Col class="col-11 d-flex align-items-center flex-column">
    <div class="title-return">
      <a href="/tasks" on:click|preventDefault={goBack}><img src="/left-arrow.svg" alt="Go back" class="go-back-arrow"/></a>
      <h1 class="page-title">New Task</h1>
    </div>
    <Notifications />
      <Col class="col-6">
        <form on:submit|preventDefault={handleSubmit}>
          <div class="mb-3">
            <label for="task_name" class="form-label">Task Name*</label>
            <input type="text" class="form-control" id="task_name" bind:value={newTask.task_name}/>
          </div>
          <div class="mb-3">
            <label for="task_descrip" class="form-label">Task Description</label>
            <textarea class="form-control" id="task_descrip" rows="3" bind:value={newTask.task_descrip}></textarea>
          </div>
          <div class="mb-3">
            <label for="task_status" class="form-label">Task Status</label>
            <select class="form-select" id="task_status" bind:value={newTask.task_status}>
              <option value="Created" selected>Created</option>
              <option value="Dropped">Dropped</option>
              <option value="Postponed">Postponed</option>
              <option value="Done">Done</option>
              <option value="Deleted">Deleted</option>
            </select>
          </div>
          <div class="mb-3">
            <label for="due_date" class="form-label">Optional due date (leave as is if it doesn't have one)</label>
            <input type="date" class="form-control" id="due_date" bind:value={newTask.due_date}/>
           </div>
          <div>
          <div class="horizontal-buttons">
            <Button on:click={goBack} block color="secondary">Go back</Button>
            <div style="margin-left: 2em;"></div>
            <Button type="submit" color="primary" block>Submit New Task</Button>
          </div>
        </form>
      </Col>
  </Col>
</main>

<style>
  :root {
    --tadashi_svelte_notifications_width: 500px;
  }
</style>