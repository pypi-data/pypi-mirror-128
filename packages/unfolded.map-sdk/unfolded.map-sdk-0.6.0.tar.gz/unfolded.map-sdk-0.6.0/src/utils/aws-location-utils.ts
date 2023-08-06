import AWS from 'aws-sdk';
import { Signer } from '@aws-amplify/core';

// API Definition here:
// - https://docs.mapbox.com/mapbox-gl-js/api/map/#map-parameters
// - https://docs.mapbox.com/mapbox-gl-js/api/properties/#requestparameters
type TransformRequest = (
  url: string,
  resourceType: string
) => {
  body?: string;
  collectResourceTiming?: boolean;
  credentials?: 'same-origin' | 'include';
  headers?: Record<string, any>;
  method?: 'GET' | 'POST' | 'PUT';
  type?: 'string' | 'json' | 'arrayBuffer';
  url: string;
};

const transformRequestFactory = (
  credentials: AWS.CognitoIdentityCredentials
) => {
  return (url: string) => {
    const signedUrl = Signer.signUrl(url, {
      access_key: credentials.accessKeyId,
      secret_key: credentials.secretAccessKey,
      session_token: credentials.sessionToken,
    });

    return { url: signedUrl };
  };
};

/**
 * Refresh Cognito credentials
 * Unauthenticated Cognito credentials are only valid for one hour:
 * https://docs.aws.amazon.com/location/latest/developerguide/authenticating-using-cognito.html#cognito-create-user-pool
 */
async function refreshCognitoCredentials(
  credentials: AWS.CognitoIdentityCredentials
) {
  await credentials.refreshPromise();

  // schedule the next credential refresh when they're about to expire
  setTimeout(
    refreshCognitoCredentials,
    credentials.expireTime.getTime() - new Date().getTime()
  );
}

export async function createAwsBasemap({
  basemapStyle,
  identityPoolId,
}: {
  basemapStyle: string;
  identityPoolId: string;
}): Promise<{
  transformRequest: TransformRequest;
  initialState: Record<string, any>;
}> {
  let transformRequest;
  let initialState;

  const region = identityPoolId.split(':')[0];
  const credentials = new AWS.CognitoIdentityCredentials(
    {
      IdentityPoolId: identityPoolId,
    },
    {
      region,
    }
  );
  transformRequest = transformRequestFactory(credentials);
  await refreshCognitoCredentials(credentials);

  initialState = {
    mapStyle: {
      mapStyles: {
        awsBasemap: {
          id: 'awsBasemap',
          label: 'AWS Basemap',
          url: transformRequest(basemapStyle).url,
        },
      },
      styleType: 'awsBasemap',
    },
  };

  return { transformRequest, initialState };
}
