import {Admin, EditGuesser, ListGuesser, Resource, ShowGuesser} from 'react-admin';
import {dataProvider} from './dataProvider';
import {authProvider} from './authProvider';

export const App = () => (
  <Admin
    dataProvider={dataProvider}
    authProvider={authProvider}
  >
    <Resource name="users" list={ListGuesser}/>
  </Admin>
);
