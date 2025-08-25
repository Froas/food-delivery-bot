/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_INTERNAL_SECRET: string
    readonly VITE_API_URL?: string

}

interface ImportMeta {
    readonly env: ImportMetaEnv
}