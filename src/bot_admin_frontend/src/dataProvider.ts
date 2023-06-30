import simpleRestProvider from 'ra-data-simple-rest';
import {fetchUtils, withLifecycleCallbacks} from "react-admin";
import {basePath} from "../env";


const httpClient = (url: string, options: any = {}) => {
  // const token = localStorage.getItem('token');
  // options.headers.set('Authorization', `Bearer ${token}`);
  // options.headers.set('Access-Control-Allow-Origin', `*`);
  // return fetchUtils.fetchJson(url, options);
    options.user = {
    authenticated: true,
    token: `Bearer ${localStorage.getItem("token")}`,
  };
  return fetchUtils.fetchJson(url, options);
};
const dataProvider = simpleRestProvider(
  `${basePath}/api/v1`,
  httpClient
);

// const dataProvider = withLifecycleCallbacks(baseDataProvider, [
//   {
//     resource: 'posts',
//     beforeCreate: async (params, dataProvider) => {
//
//       return params;
//     },
//   },
// ]);

export default dataProvider;
