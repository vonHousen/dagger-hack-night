import dagger
from dagger import dag, function, object_type


@object_type
class StoryTellerAgent:
    @function
    def write_story(
        self,
        url: str,
    ) -> dagger.Container:
        """Write a story about the code base"""
        repo_dir = dag.git(url).ref("main").tree()

        environment = (
            dag.env()
            .with_string_input("url", url, "the repo URL")
            .with_container_input(
                "builder",
                dag.container().from_("alpine").with_directory("/src", repo_dir).with_workdir("/src"),
                "a container to use for pulling the code from the repo",
            )
            .with_container_output(
                "completed", "the completed assignment in the container"
            )
        )
        

        work = (
            dag.llm()
            .with_env(environment)
            .with_prompt(
                """
                You are a story teller that loves to entertain people through engaging story telling. 
                Take a code base and create a story about the code base. Be extremely creative and stick to the Classic Story Structure.
                Be funny and engaging and exaggerate the plot. Stick to the specific content from the code base.
                Look at the code base at the current working directory and write a story about it.

                Save the story to a file called STORY.md. Create it if it doesn't exist.
                """
            )
        )

        return work.env().output("completed").as_container()