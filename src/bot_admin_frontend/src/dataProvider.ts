import simpleRestProvider from 'ra-data-simple-rest';
import {fetchUtils} from "react-admin";
import {basePath} from "../env";


const httpClient = (url: string, options: any = {}) => {
  const token = localStorage.getItem('token');
  options.headers.set('Authorization', `Bearer ${token}`);
  options.headers.set('Access-Control-Allow-Origin', `*`);
  return fetchUtils.fetchJson(url, options);
};
export const dataProvider = simpleRestProvider(
  `${basePath}/api/v1`,
  httpClient
);
