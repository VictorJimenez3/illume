// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';
import { viteStaticCopy } from 'vite-plugin-static-copy';

export default defineConfig({
  plugins: [
    react(),
    viteStaticCopy({
      targets: [
        { src: 'src/content.js', dest: '' } // copies content.js to the root of dist
      ]
    })
  ],
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        background: resolve(__dirname, 'src/background.js'),
        sidepanel: resolve(__dirname, 'src/sidepanel/index.jsx'),
        // sidepanel: resolve(__dirname, 'public/sidepanel.html'),
        quiz: resolve(__dirname, 'src/quiz/Quiz.jsx'),

        // quiz: resolve(__dirname, 'public/quiz.html')
      },
      output: {
        entryFileNames: '[name].js'
      }
    }
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  }
});
