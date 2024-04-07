<script lang="ts">
    import { Navbar, Nav, NavItem, NavLink, TabContent, TabPane } from '@sveltestrap/sveltestrap';
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { navigate } from 'svelte-routing';

    let routeId: string = $page.route.id ?? '';
    let activeTab: string;

    onMount(() => {
        switch (routeId) {
            case '/':
                activeTab = 'home';
                break;
            case '/tasks':
                activeTab = 'tasks';
                break;
            case '/about':
                activeTab = 'about';
                break;
        }
    });

    function handleTabClick(tab: string) {
        activeTab = tab;
        switch (tab) {
            case 'home':
                navigate('/');
                break;
            case 'about':
                navigate('/about');
                break;
            case 'tasks':
                navigate('/tasks');
                break;
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
</Navbar>
