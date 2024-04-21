<script lang="ts">
// @ts-nocheck
  import {Col, Row, NavBar, Button} from "@components/commonComponents";
  /*
  TODO remove this comment later
  DOCUMENTATION TO READ:
  https://kit.svelte.dev/docs/form-actions
  https://sveltestrap.js.org/?path=%2Fdocs%2Fform-formgroup--docs
  */
</script>

<main class="d-flex flex-row full-height">
  <Col class="col-1">
    <NavBar />
  </Col>
  <Col class="col-11 d-flex align-items-center flex-column">
    <h1>New Task</h1>
      <Col class="col-6">
        <form>
          <div class="mb-3">
            <label for="taskName" class="form-label">Task Name</label>
            <input type="text" class="form-control" id="taskName" />
          </div>
          <div class="mb-3">
            <label for="taskDescription" class="form-label">Task Description</label>
            <textarea class="form-control" id="taskDescription" rows="3"></textarea>
          </div>
          <div class="mb-3">
            <label for="taskStatus" class="form-label">Task Status</label>
            <select class="form-select" id="taskStatus">
              <option selected>Choose...</option>
              <option value="1">To Do</option>
              <option value="2">In Progress</option>
              <option value="3">Done</option>
            </select>
          </div>
          <Button type="submit" class="btn btn-primary">Submit</Button>
        </form>
      </Col>
  </Col>
</main>