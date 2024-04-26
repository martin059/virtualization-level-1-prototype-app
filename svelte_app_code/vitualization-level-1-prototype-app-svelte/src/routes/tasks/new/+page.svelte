<script lang="ts">
// @ts-nocheck
  import {Col, Row, NavBar, Button} from "@components/commonComponents";
  import type {Task} from "@models/Task";
  /*
  TODO remove this comment later
  DOCUMENTATION TO READ:
  https://kit.svelte.dev/docs/form-actions
  https://sveltestrap.js.org/?path=%2Fdocs%2Fform-formgroup--docs
  */

  // By default, the new task is created with the status 'Created'
  let newTask: Task = { task_name: '', task_descrip: '', task_status: 'Created' };

  async function handleSubmit() {
    console.log(newTask);
    const res = await fetch('http://localhost:5001/tasks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newTask)
    });
    const response = await res.json();
    console.log(response);
  }

  // TODO  add a notification banner or a toast to show the user that the task was created successfully and redirect to the tasks page
</script>

<main class="d-flex flex-row full-height">
  <Col class="col-1">
    <NavBar />
  </Col>
  <Col class="col-11 d-flex align-items-center flex-column">
    <h1>New Task</h1>
      <Col class="col-6">
        <form on:submit|preventDefault={handleSubmit}>
          <div class="mb-3">
            <label for="task_name" class="form-label">Task Name</label>
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
            </select>
          </div>
          <div>
            <Button type="submit" block>Submit New Task</Button>
          </div>
        </form>
      </Col>
  </Col>
</main>

<style>
</style>