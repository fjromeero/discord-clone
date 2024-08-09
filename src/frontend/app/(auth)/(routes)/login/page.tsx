"use client"

import axios, { AxiosError } from "axios";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

import { createCookie, redirectTo } from "@/app/actions";
import { Button } from "@/components/ui/button";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"


const formSchema = z.object({
    email: z.string().min(1, {message: 'Email must be filled'}).email({message: "The email is not valid"}),
    password: z.string().min(8, { message: "Password must be at least 8 characters long" }).regex(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$/,
        { message: "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character" }
    ),
})

const LoginPage = () => {

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            email: "",
            password: "",
        }
    });

    const onSubmit = async (values: z.infer<typeof formSchema>) => {
        try {
            const formData = new FormData();
            formData.append('username', values.email);
            formData.append('password', values.password);

            const result = await axios.post(`${process.env.NEXT_PUBLIC_API_HOST}/api/v1/auth/login/access-token`, formData);

            // Set the HTTP-only cookie with JWT token for the user
            createCookie({
                name: 'access_token',
                value: result.data.access_token,
                httpOnly: true,
                path: '/',
            });

            form.reset();
            redirectTo('/');
            
        } catch (error: unknown) {
            if (error instanceof AxiosError && error.response?.status === 400) {
                form.setError('email', {'message': error.response.data.detail});
                form.setError('password', {'message': error.response.data.detail});
            } else {
                console.error(error);
            }
        }
    }

    return ( 
        <div className="absolute top-0 left-0 min-h-[540px] flex items-center justify-center w-full h-full">
            <div className="bg-[#313338] p-9 flex justify-center items-center space-x-8">
                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4 w-[450px]">
                        <header className="flex flex-col items-center space-y-2">
                            <h2 className="text-white font-bold text-xl">Hi again!</h2>
                            <p className="text-[#B5BAC1] text-sm">We are very happy to see you back!</p>
                        </header>
                        <FormField
                            control={form.control}
                            name="email"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel className="text-[#B5BAC1]">Email</FormLabel>
                                    <FormControl>
                                        <Input autoComplete="off" className="bg-[#1E1F22] text-white/75 ring-0 border-0 focus-visible:ring-0 focus-visible:ring-transparent focus-visible:ring-offset-0" {...field}/>
                                    </FormControl>
                                    <FormMessage className="text-sm"/>
                                </FormItem>
                            )}
                        />
                        <FormField
                            control={form.control}
                            name="password"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel className="text-[#B5BAC1]">Password</FormLabel>
                                    <FormControl>
                                        <Input type="password" autoComplete="off" className="bg-[#1E1F22] text-white/75 ring-0 border-0 focus-visible:ring-0 focus-visible:ring-transparent focus-visible:ring-offset-0" {...field}/>
                                    </FormControl>
                                    <FormMessage className="text-sm"/>
                                </FormItem>
                            )}
                        />
                        <a className="text-sky-600 text-sm font-semibold" href="/login">Forgot your password?</a>
                        <Button
                         type="submit"
                         className="bg-[#5865F2] hover:bg-[#4A55CB] w-full"
                        >
                            Log in
                        </Button>
                        <p className="text-[#B5BAC1] text-sm">No account yet? <a className="text-sky-600 text-sm font-semibold" href="/register">Register here</a></p>
                    </form>
                </Form>
                <div>
                    <img className="w-56 h-56" src="/discord-mascot.webp"/>
                </div>
            </div>
        </div>
    );
}
 
export default LoginPage;