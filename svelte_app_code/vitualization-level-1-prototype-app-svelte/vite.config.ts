import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import alias from '@rollup/plugin-alias';
import path from 'path';

export default defineConfig({
	plugins: [
		sveltekit(),
		alias({
			entries: [
				{ find: '@components', replacement: path.resolve(__dirname, 'src/components') },
				{ find: '@models', replacement: path.resolve(__dirname, 'src/models') }
			]
		})
	]
});
