import ky from "ky";
import { cookies } from "lib/cookies";

export const api = ky.create({
  prefixUrl: process.env.API_URL,
  credentials: 'include',
  hooks: {
    beforeRequest: [
      request => {
        const token = cookies.get("access_token");
        if (token) request.headers.set("Authorization", `Bearer ${token}`);
      }
    ],
    afterResponse: [
      async (request, options, response) => {
        // logout automático se 401
        if (response.status === 401) {
          window.location.href = '/logout';
          return;
        }

        if (!response.ok) {
          let body: any;
          try {
            body = await response.json();
          } catch {
            body = { error: 'Unknown error' };
          }

          if (body.detail) {
            body.error = body.detail;
            delete body.detail;
          }

          if (!body.error) {
            body.error = 'Unknown error';
          }

          throw body;
        }
      }
    ]
  }
});
