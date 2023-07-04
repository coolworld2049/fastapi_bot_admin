import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';


export default defineConfig(({mode}) => {

  if (mode === 'development') {
    return {
      plugins: [react()],
      define: {
        'process.env': process.env,
      },
      server: {
        host: true,
        port: 3030,
      },
    };
  } else {
    return {
      plugins: [react()],
      define: {
        'process.env': process.env,
      },
      server: {
        host: true,
        port: 3030,
      },
    };
  }
});
