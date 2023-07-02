import simpleRestProvider from 'ra-data-simple-rest';
import {fetchUtils, withLifecycleCallbacks} from "react-admin";
import {basePath} from "../env";


const httpClient = (url: string, options: any = {}) => {
  options.user = {
    authenticated: true,
    token: `Bearer ${localStorage.getItem("token")}`,
  };
  return fetchUtils.fetchJson(url, options);
};
const baseDataProvider = simpleRestProvider(
  `${basePath}/api/v1`,
  httpClient
);


const dataProvider = withLifecycleCallbacks(baseDataProvider, [
  {
    /**
     * For posts update only, convert uploaded image in base 64 and attach it to
     * the `picture` sent property, with `src` and `title` attributes.
     */
    resource: 'posts',
    beforeUpdate: async (params) => {
      console.log(params)
      if (params.data.files === undefined || params.data.files == null) {
        console.log({files: params.data.files})
        return Promise.resolve(params);
      }
      const newFiles = params.data.files?.filter(
        (p: { rawFile: any; }) => p.rawFile instanceof File
      );
      const formerFiles = params.data.files?.filter(
        (p: { rawFile: any; }) => !(p.rawFile instanceof File)
      );
      console.log({callback: "beforeUpdate", newFiles: newFiles, formerFiles: formerFiles})
      return Promise.all(newFiles.map(convertFileToBase64))
        .then(base64Pictures =>
          base64Pictures.map((picture64, index) => ({
            src: picture64,
            title: `${newFiles[index].title}`,
          }))
        )
        .then(transformedNewFiles => {
            params.data.files = [
              ...transformedNewFiles,
              ...formerFiles,
            ]
            params.data.is_published = false;
            return params;
          }
        );
    },
    beforeCreate: async (params) => {
      console.log(params)
      if (params.data.files === undefined || params.data.files == null) {
        console.log({files: params.data.files})
        return Promise.resolve(params);
      }
      const newFiles = params.data.files?.filter(
        (p: { rawFile: any; }) => p.rawFile instanceof File
      );
      const formerFiles = params.data.files?.filter(
        (p: { rawFile: any; }) => !(p.rawFile instanceof File)
      );
      console.log({callback: "beforeCreate", newFiles: newFiles, formerFiles: formerFiles})
      return Promise.all(newFiles.map(convertFileToBase64))
        .then(base64Pictures =>
          base64Pictures.map((picture64, index) => ({
            src: picture64,
            title: `${newFiles[index].title}`,
          }))
        )
        .then(transformedNewFiles => {
            params.data.files = [
              ...transformedNewFiles,
              ...formerFiles,
            ]
            console.log(params)
            return params;
          }
        );
    }
  }
]);

/**
 * Convert a `File` object returned by the upload input into a base 64 string.
 * That's not the most optimized way to store images in production, but it's
 * enough to illustrate the idea of data provider decoration.
 */
const convertFileToBase64 = (file: { rawFile: Blob; }) =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file.rawFile);
  });

export default dataProvider;
