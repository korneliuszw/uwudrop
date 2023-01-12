<script lang="ts">
import { Button, FormField, Headline, Subhead, TextField, H3 } from "attractions";
import { download } from "./api";
import { page } from '$app/stores'
import { error } from "@sveltejs/kit";
import { text } from "svelte/internal";
let password: string = ""
let errorResponse: string | null = null
const submit = async () => {
    const res = await download(password, $page.params.id)
    if (res.status == 401)
        return errorResponse = "Invalid password"
    else if (res.status != 200)
        return res.json().then(({error}) => errorResponse = error)
    // Why is this so difficult?
    // Like for real, header has attachment in Disposition header so browsers should save file automatically?
    // Yet they don't, so we have to go over some blob shit
    // TODO: Find better way, redirects?
    // TODO: Figure out if this doesn't crash on large files
    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    debugger
    const filename = res.headers.get('Content-Disposition')?.split('filename=')[1]
    a.style.display = 'none'
    a.href = url
    a.download = filename ?? "unknown_file"
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
}
</script>

<div class="flex flex-col h-screen items-center justify-center">
    <Headline>This file is password-protected</Headline>
    <Subhead>Enter password below to download</Subhead>
    {#if errorResponse}
            <H3 class="text-red-500 text-xl">{errorResponse}</H3>
    {/if}
    <form on:submit={submit}>
        <FormField class="p-5" name="Password">
            <TextField type="password" bind:value={password}/>
        </FormField>
        <Button class="m-auto" type="submit" filled>Download</Button>
    </form>
</div>