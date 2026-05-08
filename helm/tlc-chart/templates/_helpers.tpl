{{/*
Expand the name of the chart.
*/}}
{{- define "tlc.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "tlc.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "tlc.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "tlc.labels" -}}
helm.sh/chart: {{ include "tlc.chart" . }}
{{ include "tlc.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: the-living-constitution
{{- end }}

{{/*
Selector labels
*/}}
{{- define "tlc.selectorLabels" -}}
app.kubernetes.io/name: {{ include "tlc.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "tlc.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "tlc.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the database URL
*/}}
{{- define "tlc.databaseUrl" -}}
{{- if .Values.postgresql.enabled }}
postgresql://{{ .Values.postgresql.auth.username }}:{{ .Values.postgresql.auth.password }}@{{ include "tlc.fullname" . }}-postgresql:5432/{{ .Values.postgresql.auth.database }}
{{- else }}
{{- .Values.externalDatabase.url }}
{{- end }}
{{- end }}

{{/*
Create the Redis URL
*/}}
{{- define "tlc.redisUrl" -}}
{{- if .Values.redis.enabled }}
redis://{{ include "tlc.fullname" . }}-redis-master:6379
{{- else }}
{{- .Values.externalRedis.url }}
{{- end }}
{{- end }}

{{/*
Constitutional AI invariants as environment variable
*/}}
{{- define "tlc.constitutionalInvariants" -}}
{{- if .Values.constitutional.invariants }}
{{- join "," .Values.constitutional.invariants }}
{{- else }}
F1-confident-false-claims,F2-phantom-completion,F3-persistence-under-correction,F4-harm-risk-coupling,F5-cross-episode-recurrence
{{- end }}
{{- end }}

{{/*
Generate certificates for TLS
*/}}
{{- define "tlc.gen-certs" -}}
{{- $altNames := list ( printf "%s.%s" (include "tlc.name" .) .Release.Namespace ) ( printf "%s.%s.svc" (include "tlc.name" .) .Release.Namespace ) -}}
{{- $ca := genCA "tlc-ca" 365 -}}
{{- $cert := genSignedCert ( include "tlc.name" . ) nil $altNames 365 $ca -}}
tls.crt: {{ $cert.Cert | b64enc }}
tls.key: {{ $cert.Key | b64enc }}
ca.crt: {{ $ca.Cert | b64enc }}
{{- end }}

{{/*
Return the proper image name
*/}}
{{- define "tlc.image" -}}
{{- $registryName := .Values.image.registry -}}
{{- $repositoryName := .Values.image.repository -}}
{{- $tag := .Values.image.tag | toString -}}
{{- if .Values.global.imageRegistry }}
    {{- $registryName = .Values.global.imageRegistry -}}
{{- end -}}
{{- if $registryName }}
    {{- printf "%s/%s:%s" $registryName $repositoryName $tag -}}
{{- else -}}
    {{- printf "%s:%s" $repositoryName $tag -}}
{{- end -}}
{{- end }}

{{/*
Return the proper image name for a specific service
*/}}
{{- define "tlc.serviceImage" -}}
{{- $registryName := .Values.image.registry -}}
{{- $repositoryName := .Values.image.repository -}}
{{- $tag := .Values.image.tag | toString -}}
{{- $service := .service -}}
{{- if .Values.global.imageRegistry }}
    {{- $registryName = .Values.global.imageRegistry -}}
{{- end -}}
{{- if $registryName }}
    {{- printf "%s/%s-%s:%s" $registryName $repositoryName $service $tag -}}
{{- else -}}
    {{- printf "%s-%s:%s" $repositoryName $service $tag -}}
{{- end -}}
{{- end }}

{{/*
Return the storage class name
*/}}
{{- define "tlc.storageClass" -}}
{{- if .Values.global.storageClass -}}
{{- .Values.global.storageClass -}}
{{- else if .Values.persistence.storageClass -}}
{{- .Values.persistence.storageClass -}}
{{- end -}}
{{- end }}

{{/*
Validate required values
*/}}
{{- define "tlc.validateValues" -}}
{{- if not .Values.secrets.anthropicApiKey }}
{{- fail "secrets.anthropicApiKey is required" }}
{{- end }}
{{- if not .Values.secrets.jwtSecret }}
{{- fail "secrets.jwtSecret is required" }}
{{- end }}
{{- if not .Values.secrets.encryptionKey }}
{{- fail "secrets.encryptionKey is required" }}
{{- end }}
{{- if not .Values.secrets.sessionSecret }}
{{- fail "secrets.sessionSecret is required" }}
{{- end }}
{{- if and .Values.postgresql.enabled (not .Values.postgresql.auth.password) }}
{{- fail "postgresql.auth.password is required when postgresql is enabled" }}
{{- end }}
{{- end }}