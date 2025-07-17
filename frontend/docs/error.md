A tree hydrated but some attributes of the server rendered HTML didn't match the client properties. This won't be patched up. This can happen if a SSR-ed Client Component used:

- A server/client branch `if (typeof window !== 'undefined')`.
- Variable input such as `Date.now()` or `Math.random()` which changes each time it's called.
- Date formatting in a user's locale which doesn't match the server.
- External changing data without sending a snapshot of it along with the HTML.
- Invalid HTML tag nesting.

It can also happen if the client has a browser extension installed which messes with the HTML before React loaded.

https://react.dev/link/hydration-mismatch

  ...
    <ClerkContextProvider initialState={null} isomorphicClerkOptions={{...}}>
      <OrganizationProvider organization={undefined}>
        <SWRConfig value={undefined}>
          <RouterTelemetry>
          <ClerkJSScript>
          <ThemeProvider attribute="class" defaultTheme="system" enableSystem={true}>
            <J attribute="class" defaultTheme="system" enableSystem={true}>
              <V attribute="class" defaultTheme="system" enableSystem={true}>
                <script>
                <ThemeToggleButton>
                <html
                  lang="en"
-                 className="light"
-                 style={{color-scheme:"light"}}
                >
                  <body
                    className="geist_e531dabc-module__QGiZLq__variable geist_mono_68a01160-module__YLcDdW__variable an..."
-                   data-new-gr-c-s-check-loaded="14.1243.0"
-                   data-gr-ext-installed=""
                  >