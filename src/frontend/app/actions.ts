"use server";

import { cookies } from "next/headers";
import { redirect } from "next/navigation";

// Definimos el tipo para las propiedades de creación de la cookie
type CookieCreationProps = {
    name: string;
    value: string;
    httpOnly?: boolean;
    path?: string;
    expires?: number | Date;
};

export const createCookie = ({ name, value, httpOnly = true, path = '/', expires }: CookieCreationProps) => {
    const options: any = {
        httpOnly,
        path,
    };

    if (expires) {
        options.expires = expires instanceof Date ? expires : new Date(expires);
    }

    cookies().set(name, value, options);
};

export const redirectTo = async (path: string) => {
    redirect(path)
}