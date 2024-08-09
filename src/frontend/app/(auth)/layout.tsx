const AuthLayout = ({children}: {children: React.ReactNode}) => {
    return (
        <div className="bg-red-950 h-full">
            <div id="background">
                <img className="fixed top-0 left-0 w-full h-full" src="/auth-background.svg"/>
            </div>
            <header>
                <img className="relative top-14 left-14" src="/discord-logo.svg"></img>
            </header>
            <div className="min-h-[80vh] w-[80vw]">
                {children}
            </div>
        </div>
    );
}

export default AuthLayout;