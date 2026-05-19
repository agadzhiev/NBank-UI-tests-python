==========================================
  kubectl — Результаты проверки кластера
  Дата: 2026-04-29 18:04:11
==========================================

## 1. Helm Release
```
NAME 	NAMESPACE	REVISION	UPDATED                            	STATUS  	CHART          	APP VERSION
nbank	default  	1       	2026-04-29 17:49:36.44885 +0300 MSK	deployed	nbank-app-1.0.0	1.0.0      
```

## 2. kubectl get pods -o wide
```
NAME                           READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
backend-86d66687dc-9x4l8       1/1     Running   0          14m   10.244.0.8   minikube   <none>           <none>
backend-86d66687dc-ngfxd       1/1     Running   0          14m   10.244.0.9   minikube   <none>           <none>
frontend-5887495c45-m6mvd      1/1     Running   0          14m   10.244.0.6   minikube   <none>           <none>
frontend-5887495c45-pzxf7      1/1     Running   0          14m   10.244.0.3   minikube   <none>           <none>
postgres-574695c557-xk8rg      1/1     Running   0          14m   10.244.0.4   minikube   <none>           <none>
selenoid-8454b964c-2lq24       1/1     Running   0          14m   10.244.0.5   minikube   <none>           <none>
selenoid-ui-66ff8dc7ff-cl2jp   1/1     Running   0          14m   10.244.0.7   minikube   <none>           <none>
```

## 3. kubectl get svc
```
NAME          TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
backend       NodePort    10.106.25.34     <none>        4111:30411/TCP   14m
frontend      NodePort    10.105.103.21    <none>        80:30000/TCP     14m
kubernetes    ClusterIP   10.96.0.1        <none>        443/TCP          16m
postgres      NodePort    10.105.86.43     <none>        5432:30432/TCP   14m
selenoid      NodePort    10.108.188.38    <none>        4444:30444/TCP   14m
selenoid-ui   NodePort    10.102.133.224   <none>        8080:30808/TCP   14m
```

## 4. kubectl get configmaps
```
NAME               DATA   AGE
backend-config     1      14m
kube-root-ca.crt   1      16m
postgres-config    1      14m
selenoid-config    1      14m
```

## 5. kubectl describe configmap postgres-config
```
Name:         postgres-config
Namespace:    default
Labels:       app=postgres
              app.kubernetes.io/managed-by=Helm
Annotations:  meta.helm.sh/release-name: nbank
              meta.helm.sh/release-namespace: default

Data
====
POSTGRES_DB:
----
nbank


BinaryData
====

Events:  <none>
```

## 6. kubectl describe configmap backend-config
```
Name:         backend-config
Namespace:    default
Labels:       app=backend
              app.kubernetes.io/managed-by=Helm
Annotations:  meta.helm.sh/release-name: nbank
              meta.helm.sh/release-namespace: default

Data
====
SPRING_DATASOURCE_URL:
----
jdbc:postgresql://postgres:5432/nbank


BinaryData
====

Events:  <none>
```

## 7. kubectl describe configmap selenoid-config
```
Name:         selenoid-config
Namespace:    default
Labels:       app=selenoid
              app.kubernetes.io/managed-by=Helm
Annotations:  meta.helm.sh/release-name: nbank
              meta.helm.sh/release-namespace: default

Data
====
browsers.json:
----
{
  "chrome": {
    "default": "131.0",
    "versions": {
      "131.0": {
        "image": "selenoid/vnc_chrome:131.0",
        "port": "4444",
        "path": "/"
      }
    }
  },
  "firefox": {
    "default": "133.0",
    "versions": {
      "133.0": {
        "image": "selenoid/vnc_firefox:133.0",
        "port": "4444",
        "path": "/wd/hub"
      }
    }
  }
}



BinaryData
====

Events:  <none>
```

## 8. kubectl get secrets
```
NAME                          TYPE                 DATA   AGE
postgres-secret               Opaque               2      14m
sh.helm.release.v1.nbank.v1   helm.sh/release.v1   1      14m
```

## 9. kubectl describe secret postgres-secret
```
Name:         postgres-secret
Namespace:    default
Labels:       app=postgres
              app.kubernetes.io/managed-by=Helm
Annotations:  meta.helm.sh/release-name: nbank
              meta.helm.sh/release-namespace: default

Type:  Opaque

Data
====
POSTGRES_PASSWORD:  8 bytes
POSTGRES_USER:      8 bytes
```

## 10. kubectl logs — postgres (последние 20 строк)
```
waiting for server to shut down....2026-04-29 14:51:12.648 UTC [41] LOG:  received fast shutdown request
2026-04-29 14:51:12.649 UTC [41] LOG:  aborting any active transactions
2026-04-29 14:51:12.651 UTC [41] LOG:  background worker "logical replication launcher" (PID 47) exited with exit code 1
2026-04-29 14:51:12.652 UTC [42] LOG:  shutting down
2026-04-29 14:51:12.652 UTC [42] LOG:  checkpoint starting: shutdown immediate
2026-04-29 14:51:12.675 UTC [42] LOG:  checkpoint complete: wrote 921 buffers (5.6%); 0 WAL file(s) added, 0 removed, 0 recycled; write=0.006 s, sync=0.015 s, total=0.023 s; sync files=301, longest=0.007 s, average=0.001 s; distance=4238 kB, estimate=4238 kB
2026-04-29 14:51:12.677 UTC [41] LOG:  database system is shut down
 done
server stopped

PostgreSQL init process complete; ready for start up.

2026-04-29 14:51:12.760 UTC [1] LOG:  starting PostgreSQL 15.17 on aarch64-unknown-linux-musl, compiled by gcc (Alpine 15.2.0) 15.2.0, 64-bit
2026-04-29 14:51:12.760 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
2026-04-29 14:51:12.760 UTC [1] LOG:  listening on IPv6 address "::", port 5432
2026-04-29 14:51:12.762 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2026-04-29 14:51:12.764 UTC [57] LOG:  database system was shut down at 2026-04-29 14:51:12 UTC
2026-04-29 14:51:12.766 UTC [1] LOG:  database system is ready to accept connections
2026-04-29 14:56:12.868 UTC [55] LOG:  checkpoint starting: time
2026-04-29 14:56:28.228 UTC [55] LOG:  checkpoint complete: wrote 155 buffers (0.9%); 0 WAL file(s) added, 0 removed, 0 recycled; write=15.323 s, sync=0.024 s, total=15.361 s; sync files=79, longest=0.010 s, average=0.001 s; distance=573 kB, estimate=573 kB
```

## 11. kubectl logs — backend (последние 20 строк)
```
{"timestamp":"2026-04-29T14:54:59.19589946Z","logger_name":"org.flywaydb.core.internal.command.DbValidate","thread_name":"main","level":"INFO","message":"Successfully validated 3 migrations (execution time 00:00.014s)"}
{"timestamp":"2026-04-29T14:54:59.215177844Z","logger_name":"org.flywaydb.core.internal.command.DbMigrate","thread_name":"main","level":"INFO","message":"Current version of schema \"public\": 3"}
{"timestamp":"2026-04-29T14:54:59.216476478Z","logger_name":"org.flywaydb.core.internal.command.DbMigrate","thread_name":"main","level":"INFO","message":"Schema \"public\" is up to date. No migration necessary."}
{"timestamp":"2026-04-29T14:54:59.305880096Z","logger_name":"org.hibernate.jpa.internal.util.LogHelper","thread_name":"main","level":"INFO","message":"HHH000204: Processing PersistenceUnitInfo [name: default]"}
{"timestamp":"2026-04-29T14:54:59.360127429Z","logger_name":"org.hibernate.Version","thread_name":"main","level":"INFO","message":"HHH000412: Hibernate ORM core version 6.4.4.Final"}
{"timestamp":"2026-04-29T14:54:59.386600528Z","logger_name":"org.hibernate.cache.internal.RegionFactoryInitiator","thread_name":"main","level":"INFO","message":"HHH000026: Second-level cache disabled"}
{"timestamp":"2026-04-29T14:54:59.526774039Z","logger_name":"org.springframework.orm.jpa.persistenceunit.SpringPersistenceUnitInfo","thread_name":"main","level":"INFO","message":"No LoadTimeWeaver setup: ignoring JPA class transformer"}
{"timestamp":"2026-04-29T14:54:59.563010164Z","logger_name":"org.hibernate.orm.deprecation","thread_name":"main","level":"WARN","message":"HHH90000025: PostgreSQLDialect does not need to be specified explicitly using 'hibernate.dialect' (remove the property setting and it will be selected by default)"}
{"timestamp":"2026-04-29T14:55:00.11359897Z","logger_name":"org.hibernate.engine.transaction.jta.platform.internal.JtaPlatformInitiator","thread_name":"main","level":"INFO","message":"HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)"}
{"timestamp":"2026-04-29T14:55:00.135612622Z","logger_name":"org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean","thread_name":"main","level":"INFO","message":"Initialized JPA EntityManagerFactory for persistence unit 'default'"}
🧪 MeterRegistry class = io.micrometer.prometheus.PrometheusMeterRegistry
{"timestamp":"2026-04-29T14:55:00.45213431Z","logger_name":"org.springframework.data.jpa.repository.query.QueryEnhancerFactory","thread_name":"main","level":"INFO","message":"Hibernate is in classpath; If applicable, HQL parser will be used."}
{"timestamp":"2026-04-29T14:55:00.882086407Z","logger_name":"org.springframework.boot.autoconfigure.orm.jpa.JpaBaseConfiguration$JpaWebConfiguration","thread_name":"main","level":"WARN","message":"spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning"}
{"timestamp":"2026-04-29T14:55:01.181636144Z","logger_name":"org.springframework.boot.actuate.endpoint.web.EndpointLinksResolver","thread_name":"main","level":"INFO","message":"Exposing 3 endpoint(s) beneath base path '/actuator'"}
{"timestamp":"2026-04-29T14:55:01.216233884Z","logger_name":"org.springframework.security.web.DefaultSecurityFilterChain","thread_name":"main","level":"INFO","message":"Will secure any request with [org.springframework.security.web.session.DisableEncodeUrlFilter@7e2723d2, org.springframework.security.web.context.request.async.WebAsyncManagerIntegrationFilter@2b0061b7, org.springframework.security.web.context.SecurityContextHolderFilter@29e63bc3, org.springframework.security.web.header.HeaderWriterFilter@75d70348, org.springframework.web.filter.CorsFilter@72dc0d72, org.springframework.security.web.authentication.logout.LogoutFilter@3d62648d, org.springframework.security.web.authentication.www.BasicAuthenticationFilter@7ce299c6, org.springframework.security.web.savedrequest.RequestCacheAwareFilter@1f6b9ab7, org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter@3d872a12, org.springframework.security.web.authentication.AnonymousAuthenticationFilter@79176fe4, org.springframework.security.web.access.ExceptionTranslationFilter@5a0379e2, org.springframework.security.web.access.intercept.AuthorizationFilter@5331be15]"}
{"timestamp":"2026-04-29T14:55:01.518728975Z","logger_name":"org.springframework.boot.web.embedded.tomcat.TomcatWebServer","thread_name":"main","level":"INFO","message":"Tomcat started on port 4111 (http) with context path ''"}
{"timestamp":"2026-04-29T14:55:01.535568967Z","logger_name":"me.nobugs.bank.BankApplication","thread_name":"main","level":"INFO","message":"Started BankApplication in 4.513 seconds (process running for 4.777)"}
{"timestamp":"2026-04-29T14:55:13.53185531Z","logger_name":"org.apache.catalina.core.ContainerBase.[Tomcat].[localhost].[/]","thread_name":"http-nio-4111-exec-1","level":"INFO","message":"Initializing Spring DispatcherServlet 'dispatcherServlet'"}
{"timestamp":"2026-04-29T14:55:13.532109103Z","logger_name":"org.springframework.web.servlet.DispatcherServlet","thread_name":"http-nio-4111-exec-1","level":"INFO","message":"Initializing Servlet 'dispatcherServlet'"}
{"timestamp":"2026-04-29T14:55:13.533078193Z","logger_name":"org.springframework.web.servlet.DispatcherServlet","thread_name":"http-nio-4111-exec-1","level":"INFO","message":"Completed initialization in 1 ms"}
{"timestamp":"2026-04-29T14:54:17.691497062Z","logger_name":"org.flywaydb.core.internal.command.DbMigrate","thread_name":"main","level":"INFO","message":"Migrating schema \"public\" to version \"2 - Insert sample data\""}
{"timestamp":"2026-04-29T14:54:17.702915598Z","logger_name":"org.flywaydb.core.internal.command.DbMigrate","thread_name":"main","level":"INFO","message":"Migrating schema \"public\" to version \"3 - Fix password hashes\""}
{"timestamp":"2026-04-29T14:54:17.710734527Z","logger_name":"org.flywaydb.core.internal.command.DbMigrate","thread_name":"main","level":"INFO","message":"Successfully applied 3 migrations to schema \"public\", now at version v3 (execution time 00:00.036s)"}
{"timestamp":"2026-04-29T14:54:17.785318912Z","logger_name":"org.hibernate.jpa.internal.util.LogHelper","thread_name":"main","level":"INFO","message":"HHH000204: Processing PersistenceUnitInfo [name: default]"}
{"timestamp":"2026-04-29T14:54:17.823969093Z","logger_name":"org.hibernate.Version","thread_name":"main","level":"INFO","message":"HHH000412: Hibernate ORM core version 6.4.4.Final"}
{"timestamp":"2026-04-29T14:54:17.847501921Z","logger_name":"org.hibernate.cache.internal.RegionFactoryInitiator","thread_name":"main","level":"INFO","message":"HHH000026: Second-level cache disabled"}
{"timestamp":"2026-04-29T14:54:17.964746849Z","logger_name":"org.springframework.orm.jpa.persistenceunit.SpringPersistenceUnitInfo","thread_name":"main","level":"INFO","message":"No LoadTimeWeaver setup: ignoring JPA class transformer"}
{"timestamp":"2026-04-29T14:54:17.997628115Z","logger_name":"org.hibernate.orm.deprecation","thread_name":"main","level":"WARN","message":"HHH90000025: PostgreSQLDialect does not need to be specified explicitly using 'hibernate.dialect' (remove the property setting and it will be selected by default)"}
{"timestamp":"2026-04-29T14:54:18.559840339Z","logger_name":"org.hibernate.engine.transaction.jta.platform.internal.JtaPlatformInitiator","thread_name":"main","level":"INFO","message":"HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)"}
{"timestamp":"2026-04-29T14:54:18.586768732Z","logger_name":"org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean","thread_name":"main","level":"INFO","message":"Initialized JPA EntityManagerFactory for persistence unit 'default'"}
🧪 MeterRegistry class = io.micrometer.prometheus.PrometheusMeterRegistry
{"timestamp":"2026-04-29T14:54:18.784045333Z","logger_name":"org.springframework.data.jpa.repository.query.QueryEnhancerFactory","thread_name":"main","level":"INFO","message":"Hibernate is in classpath; If applicable, HQL parser will be used."}
{"timestamp":"2026-04-29T14:54:19.234012956Z","logger_name":"org.springframework.boot.autoconfigure.orm.jpa.JpaBaseConfiguration$JpaWebConfiguration","thread_name":"main","level":"WARN","message":"spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning"}
{"timestamp":"2026-04-29T14:54:19.4497436Z","logger_name":"org.springframework.boot.actuate.endpoint.web.EndpointLinksResolver","thread_name":"main","level":"INFO","message":"Exposing 3 endpoint(s) beneath base path '/actuator'"}
{"timestamp":"2026-04-29T14:54:19.482755784Z","logger_name":"org.springframework.security.web.DefaultSecurityFilterChain","thread_name":"main","level":"INFO","message":"Will secure any request with [org.springframework.security.web.session.DisableEncodeUrlFilter@32578bc0, org.springframework.security.web.context.request.async.WebAsyncManagerIntegrationFilter@9d09c6f, org.springframework.security.web.context.SecurityContextHolderFilter@2a09e0d4, org.springframework.security.web.header.HeaderWriterFilter@ca5456e, org.springframework.web.filter.CorsFilter@2bed4ed, org.springframework.security.web.authentication.logout.LogoutFilter@101d4a4e, org.springframework.security.web.authentication.www.BasicAuthenticationFilter@15402cf4, org.springframework.security.web.savedrequest.RequestCacheAwareFilter@4064cd60, org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter@e74914d, org.springframework.security.web.authentication.AnonymousAuthenticationFilter@57e17da, org.springframework.security.web.access.ExceptionTranslationFilter@23247b4c, org.springframework.security.web.access.intercept.AuthorizationFilter@5dca9fd8]"}
{"timestamp":"2026-04-29T14:54:19.75869559Z","logger_name":"org.springframework.boot.web.embedded.tomcat.TomcatWebServer","thread_name":"main","level":"INFO","message":"Tomcat started on port 4111 (http) with context path ''"}
{"timestamp":"2026-04-29T14:54:19.766757187Z","logger_name":"me.nobugs.bank.BankApplication","thread_name":"main","level":"INFO","message":"Started BankApplication in 4.431 seconds (process running for 4.728)"}
{"timestamp":"2026-04-29T14:54:33.111661517Z","logger_name":"org.apache.catalina.core.ContainerBase.[Tomcat].[localhost].[/]","thread_name":"http-nio-4111-exec-1","level":"INFO","message":"Initializing Spring DispatcherServlet 'dispatcherServlet'"}
{"timestamp":"2026-04-29T14:54:33.112091229Z","logger_name":"org.springframework.web.servlet.DispatcherServlet","thread_name":"http-nio-4111-exec-1","level":"INFO","message":"Initializing Servlet 'dispatcherServlet'"}
{"timestamp":"2026-04-29T14:54:33.113379237Z","logger_name":"org.springframework.web.servlet.DispatcherServlet","thread_name":"http-nio-4111-exec-1","level":"INFO","message":"Completed initialization in 1 ms"}
```

## 12. kubectl logs — frontend (последние 20 строк)
```
10.244.0.1 - - [29/Apr/2026:15:03:07 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:11 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:16 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:17 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:21 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:26 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:27 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:31 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:36 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:37 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:41 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:46 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:47 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:51 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:56 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:57 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:04:01 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:04:06 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:04:07 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:04:11 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:07 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:07 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:12 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:17 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:17 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:22 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:27 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:27 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:32 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:37 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:37 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:42 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:47 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:47 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:52 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:57 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:03:57 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:04:02 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:04:07 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
10.244.0.1 - - [29/Apr/2026:15:04:07 +0000] "GET / HTTP/1.1" 200 648 "-" "kube-probe/1.35"
```

## 13. kubectl logs — selenoid (последние 20 строк)
```
2026/04/29 14:52:47 [-] [INIT] [Loading configuration files...]
2026/04/29 14:52:47 [-] [INIT] [Loaded configuration from /etc/selenoid/browsers.json]
2026/04/29 14:52:47 [-] [INIT] [Video Dir: /opt/selenoid/video]
2026/04/29 14:52:47 [-] [INIT] [Did not manage to determine your Docker API version - using default version: 1.45]
2026/04/29 14:52:47 [-] [INIT] [Timezone: UTC]
2026/04/29 14:52:47 [-] [INIT] [Listening on :4444]
```

## 14. kubectl logs — selenoid-ui (последние 20 строк)
```
2026/04/29 14:52:57 [INIT] [Listening on :8080]
```

## 15. Масштабирование backend до 3 реплик
```
deployment.apps/backend scaled
NAME                       READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
backend-86d66687dc-9x4l8   1/1     Running   0          14m   10.244.0.8    minikube   <none>           <none>
backend-86d66687dc-jmdvf   0/1     Running   0          5s    10.244.0.12   minikube   <none>           <none>
backend-86d66687dc-ngfxd   1/1     Running   0          14m   10.244.0.9    minikube   <none>           <none>
```

## 16. Масштабирование frontend до 3 реплик
```
deployment.apps/frontend scaled
NAME                        READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
frontend-5887495c45-9kv28   0/1     Running   0          5s    10.244.0.13   minikube   <none>           <none>
frontend-5887495c45-m6mvd   1/1     Running   0          14m   10.244.0.6    minikube   <none>           <none>
frontend-5887495c45-pzxf7   1/1     Running   0          14m   10.244.0.3    minikube   <none>           <none>
```

## 17. Статус после масштабирования
```
NAME                           READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
backend-86d66687dc-9x4l8       1/1     Running   0          14m   10.244.0.8    minikube   <none>           <none>
backend-86d66687dc-jmdvf       1/1     Running   0          20s   10.244.0.12   minikube   <none>           <none>
backend-86d66687dc-ngfxd       1/1     Running   0          14m   10.244.0.9    minikube   <none>           <none>
frontend-5887495c45-9kv28      1/1     Running   0          15s   10.244.0.13   minikube   <none>           <none>
frontend-5887495c45-m6mvd      1/1     Running   0          14m   10.244.0.6    minikube   <none>           <none>
frontend-5887495c45-pzxf7      1/1     Running   0          14m   10.244.0.3    minikube   <none>           <none>
postgres-574695c557-xk8rg      1/1     Running   0          14m   10.244.0.4    minikube   <none>           <none>
selenoid-8454b964c-2lq24       1/1     Running   0          14m   10.244.0.5    minikube   <none>           <none>
selenoid-ui-66ff8dc7ff-cl2jp   1/1     Running   0          14m   10.244.0.7    minikube   <none>           <none>
```

## 18. Масштабирование обратно (backend=2, frontend=2)
```
deployment.apps/backend scaled
deployment.apps/frontend scaled
NAME                           READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
backend-86d66687dc-9x4l8       1/1     Running   0          15m   10.244.0.8   minikube   <none>           <none>
backend-86d66687dc-ngfxd       1/1     Running   0          15m   10.244.0.9   minikube   <none>           <none>
frontend-5887495c45-m6mvd      1/1     Running   0          15m   10.244.0.6   minikube   <none>           <none>
frontend-5887495c45-pzxf7      1/1     Running   0          15m   10.244.0.3   minikube   <none>           <none>
postgres-574695c557-xk8rg      1/1     Running   0          15m   10.244.0.4   minikube   <none>           <none>
selenoid-8454b964c-2lq24       1/1     Running   0          15m   10.244.0.5   minikube   <none>           <none>
selenoid-ui-66ff8dc7ff-cl2jp   1/1     Running   0          15m   10.244.0.7   minikube   <none>           <none>
```

## 19. kubectl describe svc backend
```
Name:                     backend
Namespace:                default
Labels:                   app=backend
                          app.kubernetes.io/managed-by=Helm
Annotations:              meta.helm.sh/release-name: nbank
                          meta.helm.sh/release-namespace: default
Selector:                 app=backend
Type:                     NodePort
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.106.25.34
IPs:                      10.106.25.34
Port:                     <unset>  4111/TCP
TargetPort:               4111/TCP
NodePort:                 <unset>  30411/TCP
Endpoints:                10.244.0.8:4111,10.244.0.9:4111
Session Affinity:         None
External Traffic Policy:  Cluster
Internal Traffic Policy:  Cluster
Events:                   <none>
```

## 20. kubectl describe svc frontend
```
Name:                     frontend
Namespace:                default
Labels:                   app=frontend
                          app.kubernetes.io/managed-by=Helm
Annotations:              meta.helm.sh/release-name: nbank
                          meta.helm.sh/release-namespace: default
Selector:                 app=frontend
Type:                     NodePort
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.105.103.21
IPs:                      10.105.103.21
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  30000/TCP
Endpoints:                10.244.0.3:80,10.244.0.6:80
Session Affinity:         None
External Traffic Policy:  Cluster
Internal Traffic Policy:  Cluster
Events:                   <none>
```

## 21. Minikube service URLs
```
192.168.49.2
```

==========================================
  Проверка завершена успешно
==========================================
