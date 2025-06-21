import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/lara-light-green/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';

import Card from 'primevue/card';
import Button from 'primevue/button';
import Avatar from 'primevue/avatar';
import Divider from 'primevue/divider';

const app = createApp(App)
app.use(PrimeVue)
app.mount('#app')
app.component('Card', Card)
app.component('Button', Button)
app.component('Avatar', Avatar)
app.component('Divider', Divider)

