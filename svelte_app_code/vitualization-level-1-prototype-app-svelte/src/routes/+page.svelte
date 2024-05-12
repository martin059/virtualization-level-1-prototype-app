<script lang="ts">
  // @ts-nocheck
  import { Col, NavBar, Button } from '@components/commonComponents';
  import { goto } from '$app/navigation';

  function goToTasks() {
    goto('/tasks');
  }
  function goToAbout() {
    goto('/about');
  }
</script>

<main class="d-flex flex-row full-height">
  <Col class="col-1">
    <NavBar />
  </Col>
  <Col class="col-11 d-flex align-items-center flex-column">
    <h1 class="page-title"><img src="/ToDo-icon.svg" alt="to-do-logo-sample" id="logo"> Svelte Front End ToDo App</h1>
    <div class="full-height centered-vertically increased-txt-size">
      <div class="central-div">
        <h2>Welcome to the Svelte Front End ToDo App!</h2>
        <div style="margin-bottom: 30px;"></div>
        <Button on:click={goToTasks} color="primary" block >Go to View Task</Button>
        <div style="margin-bottom: 15px;"></div>
        <Button on:click={goToAbout} color="secondary" block class='main-button'>Learn more about this App!</Button>
      </div>
    </div>
  </Col>
</main>

<style>
  #logo {
    width: 1.75em;
    height: 1.75em;
  }
  .central-div {
    margin-top: 40%;
  }
</style>
