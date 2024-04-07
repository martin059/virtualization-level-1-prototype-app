<script lang="ts">
    import { Navbar, Nav, NavItem, NavLink, TabContent, TabPane } from '@sveltestrap/sveltestrap';
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { navigate } from 'svelte-routing';

    let routeId: string = $page.route.id ?? '';
    let activeTab = 'task';

    onMount(() => {
        console.log('routeId:', routeId);
    });

    function handleTabClick(tab: string) {
        activeTab = tab;
        if (tab === 'home') {
            navigate('/');
        }
        if (tab === 'about') {
            navigate('/about');
        }
        if (tab === 'tasks') {
            navigate('/tasks');
        }
    }
</script>

<Navbar color="light" light expand="md">
    <Nav tabs>
        <NavItem>
            <NavLink active={activeTab === 'home'} on:click={() => handleTabClick('home')}>
                Home
            </NavLink>
        </NavItem>
        <NavItem>
            <NavLink active={activeTab === 'tasks'} on:click={() => handleTabClick('tasks')}>
                Tasks
            </NavLink>
        </NavItem>
        <NavItem>
            <NavLink active={activeTab === 'about'} on:click={() => handleTabClick('about')}>
                About
            </NavLink>
        </NavItem>
    </Nav>
    <TabContent activeTab={activeTab}>
        <TabPane tabId="home">
            <!-- Content for the 'Home' tab -->
        </TabPane>
        <TabPane tabId="task">
            <!-- Content for the 'Task' tab -->
        </TabPane>
        <TabPane tabId="about">
            <!-- Content for the 'About' tab -->
        </TabPane>
    </TabContent>
</Navbar>
