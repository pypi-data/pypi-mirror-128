# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['GoRepositoryArgs', 'GoRepository']

@pulumi.input_type
class GoRepositoryArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 repositories: pulumi.Input[Sequence[pulumi.Input[str]]],
                 artifactory_requests_can_retrieve_remote_artifacts: Optional[pulumi.Input[bool]] = None,
                 default_deployment_repo: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 excludes_pattern: Optional[pulumi.Input[str]] = None,
                 external_dependencies_enabled: Optional[pulumi.Input[bool]] = None,
                 external_dependencies_patterns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 includes_pattern: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 repo_layout_ref: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a GoRepository resource.
        :param pulumi.Input[str] excludes_pattern: List of artifact patterns to exclude when evaluating artifact requests, in the form of x/y/**/z/*.By default no
               artifacts are excluded.
        :param pulumi.Input[bool] external_dependencies_enabled: . Shorthand for "Enable 'go-import' Meta Tags" on the UI. This must be set to true in order to use the allow list
        :param pulumi.Input[Sequence[pulumi.Input[str]]] external_dependencies_patterns: - 'go-import' Allow List on the UI.
        :param pulumi.Input[str] includes_pattern: List of artifact patterns to include when evaluating artifact requests in the form of x/y/**/z/*. When used, only
               artifacts matching one of the include patterns are served. By default, all artifacts are included (**/*).
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "repositories", repositories)
        if artifactory_requests_can_retrieve_remote_artifacts is not None:
            pulumi.set(__self__, "artifactory_requests_can_retrieve_remote_artifacts", artifactory_requests_can_retrieve_remote_artifacts)
        if default_deployment_repo is not None:
            pulumi.set(__self__, "default_deployment_repo", default_deployment_repo)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if excludes_pattern is not None:
            pulumi.set(__self__, "excludes_pattern", excludes_pattern)
        if external_dependencies_enabled is not None:
            pulumi.set(__self__, "external_dependencies_enabled", external_dependencies_enabled)
        if external_dependencies_patterns is not None:
            pulumi.set(__self__, "external_dependencies_patterns", external_dependencies_patterns)
        if includes_pattern is not None:
            pulumi.set(__self__, "includes_pattern", includes_pattern)
        if notes is not None:
            pulumi.set(__self__, "notes", notes)
        if repo_layout_ref is not None:
            pulumi.set(__self__, "repo_layout_ref", repo_layout_ref)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def repositories(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        return pulumi.get(self, "repositories")

    @repositories.setter
    def repositories(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "repositories", value)

    @property
    @pulumi.getter(name="artifactoryRequestsCanRetrieveRemoteArtifacts")
    def artifactory_requests_can_retrieve_remote_artifacts(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "artifactory_requests_can_retrieve_remote_artifacts")

    @artifactory_requests_can_retrieve_remote_artifacts.setter
    def artifactory_requests_can_retrieve_remote_artifacts(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "artifactory_requests_can_retrieve_remote_artifacts", value)

    @property
    @pulumi.getter(name="defaultDeploymentRepo")
    def default_deployment_repo(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "default_deployment_repo")

    @default_deployment_repo.setter
    def default_deployment_repo(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_deployment_repo", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="excludesPattern")
    def excludes_pattern(self) -> Optional[pulumi.Input[str]]:
        """
        List of artifact patterns to exclude when evaluating artifact requests, in the form of x/y/**/z/*.By default no
        artifacts are excluded.
        """
        return pulumi.get(self, "excludes_pattern")

    @excludes_pattern.setter
    def excludes_pattern(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "excludes_pattern", value)

    @property
    @pulumi.getter(name="externalDependenciesEnabled")
    def external_dependencies_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        . Shorthand for "Enable 'go-import' Meta Tags" on the UI. This must be set to true in order to use the allow list
        """
        return pulumi.get(self, "external_dependencies_enabled")

    @external_dependencies_enabled.setter
    def external_dependencies_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "external_dependencies_enabled", value)

    @property
    @pulumi.getter(name="externalDependenciesPatterns")
    def external_dependencies_patterns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        - 'go-import' Allow List on the UI.
        """
        return pulumi.get(self, "external_dependencies_patterns")

    @external_dependencies_patterns.setter
    def external_dependencies_patterns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "external_dependencies_patterns", value)

    @property
    @pulumi.getter(name="includesPattern")
    def includes_pattern(self) -> Optional[pulumi.Input[str]]:
        """
        List of artifact patterns to include when evaluating artifact requests in the form of x/y/**/z/*. When used, only
        artifacts matching one of the include patterns are served. By default, all artifacts are included (**/*).
        """
        return pulumi.get(self, "includes_pattern")

    @includes_pattern.setter
    def includes_pattern(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "includes_pattern", value)

    @property
    @pulumi.getter
    def notes(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "notes")

    @notes.setter
    def notes(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "notes", value)

    @property
    @pulumi.getter(name="repoLayoutRef")
    def repo_layout_ref(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "repo_layout_ref")

    @repo_layout_ref.setter
    def repo_layout_ref(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "repo_layout_ref", value)


@pulumi.input_type
class _GoRepositoryState:
    def __init__(__self__, *,
                 artifactory_requests_can_retrieve_remote_artifacts: Optional[pulumi.Input[bool]] = None,
                 default_deployment_repo: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 excludes_pattern: Optional[pulumi.Input[str]] = None,
                 external_dependencies_enabled: Optional[pulumi.Input[bool]] = None,
                 external_dependencies_patterns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 includes_pattern: Optional[pulumi.Input[str]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 package_type: Optional[pulumi.Input[str]] = None,
                 repo_layout_ref: Optional[pulumi.Input[str]] = None,
                 repositories: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering GoRepository resources.
        :param pulumi.Input[str] excludes_pattern: List of artifact patterns to exclude when evaluating artifact requests, in the form of x/y/**/z/*.By default no
               artifacts are excluded.
        :param pulumi.Input[bool] external_dependencies_enabled: . Shorthand for "Enable 'go-import' Meta Tags" on the UI. This must be set to true in order to use the allow list
        :param pulumi.Input[Sequence[pulumi.Input[str]]] external_dependencies_patterns: - 'go-import' Allow List on the UI.
        :param pulumi.Input[str] includes_pattern: List of artifact patterns to include when evaluating artifact requests in the form of x/y/**/z/*. When used, only
               artifacts matching one of the include patterns are served. By default, all artifacts are included (**/*).
        """
        if artifactory_requests_can_retrieve_remote_artifacts is not None:
            pulumi.set(__self__, "artifactory_requests_can_retrieve_remote_artifacts", artifactory_requests_can_retrieve_remote_artifacts)
        if default_deployment_repo is not None:
            pulumi.set(__self__, "default_deployment_repo", default_deployment_repo)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if excludes_pattern is not None:
            pulumi.set(__self__, "excludes_pattern", excludes_pattern)
        if external_dependencies_enabled is not None:
            pulumi.set(__self__, "external_dependencies_enabled", external_dependencies_enabled)
        if external_dependencies_patterns is not None:
            pulumi.set(__self__, "external_dependencies_patterns", external_dependencies_patterns)
        if includes_pattern is not None:
            pulumi.set(__self__, "includes_pattern", includes_pattern)
        if key is not None:
            pulumi.set(__self__, "key", key)
        if notes is not None:
            pulumi.set(__self__, "notes", notes)
        if package_type is not None:
            pulumi.set(__self__, "package_type", package_type)
        if repo_layout_ref is not None:
            pulumi.set(__self__, "repo_layout_ref", repo_layout_ref)
        if repositories is not None:
            pulumi.set(__self__, "repositories", repositories)

    @property
    @pulumi.getter(name="artifactoryRequestsCanRetrieveRemoteArtifacts")
    def artifactory_requests_can_retrieve_remote_artifacts(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "artifactory_requests_can_retrieve_remote_artifacts")

    @artifactory_requests_can_retrieve_remote_artifacts.setter
    def artifactory_requests_can_retrieve_remote_artifacts(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "artifactory_requests_can_retrieve_remote_artifacts", value)

    @property
    @pulumi.getter(name="defaultDeploymentRepo")
    def default_deployment_repo(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "default_deployment_repo")

    @default_deployment_repo.setter
    def default_deployment_repo(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_deployment_repo", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="excludesPattern")
    def excludes_pattern(self) -> Optional[pulumi.Input[str]]:
        """
        List of artifact patterns to exclude when evaluating artifact requests, in the form of x/y/**/z/*.By default no
        artifacts are excluded.
        """
        return pulumi.get(self, "excludes_pattern")

    @excludes_pattern.setter
    def excludes_pattern(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "excludes_pattern", value)

    @property
    @pulumi.getter(name="externalDependenciesEnabled")
    def external_dependencies_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        . Shorthand for "Enable 'go-import' Meta Tags" on the UI. This must be set to true in order to use the allow list
        """
        return pulumi.get(self, "external_dependencies_enabled")

    @external_dependencies_enabled.setter
    def external_dependencies_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "external_dependencies_enabled", value)

    @property
    @pulumi.getter(name="externalDependenciesPatterns")
    def external_dependencies_patterns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        - 'go-import' Allow List on the UI.
        """
        return pulumi.get(self, "external_dependencies_patterns")

    @external_dependencies_patterns.setter
    def external_dependencies_patterns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "external_dependencies_patterns", value)

    @property
    @pulumi.getter(name="includesPattern")
    def includes_pattern(self) -> Optional[pulumi.Input[str]]:
        """
        List of artifact patterns to include when evaluating artifact requests in the form of x/y/**/z/*. When used, only
        artifacts matching one of the include patterns are served. By default, all artifacts are included (**/*).
        """
        return pulumi.get(self, "includes_pattern")

    @includes_pattern.setter
    def includes_pattern(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "includes_pattern", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def notes(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "notes")

    @notes.setter
    def notes(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "notes", value)

    @property
    @pulumi.getter(name="packageType")
    def package_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "package_type")

    @package_type.setter
    def package_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "package_type", value)

    @property
    @pulumi.getter(name="repoLayoutRef")
    def repo_layout_ref(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "repo_layout_ref")

    @repo_layout_ref.setter
    def repo_layout_ref(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "repo_layout_ref", value)

    @property
    @pulumi.getter
    def repositories(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "repositories")

    @repositories.setter
    def repositories(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "repositories", value)


class GoRepository(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 artifactory_requests_can_retrieve_remote_artifacts: Optional[pulumi.Input[bool]] = None,
                 default_deployment_repo: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 excludes_pattern: Optional[pulumi.Input[str]] = None,
                 external_dependencies_enabled: Optional[pulumi.Input[bool]] = None,
                 external_dependencies_patterns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 includes_pattern: Optional[pulumi.Input[str]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 repo_layout_ref: Optional[pulumi.Input[str]] = None,
                 repositories: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        ## # Artifactory Virtual Go Repository Resource

        Provides an Artifactory virtual repository resource, but with specific go lang features. This should be preferred over the original
        one-size-fits-all `VirtualRepository`.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_artifactory as artifactory

        baz_go = artifactory.GoRepository("baz-go",
            description="A test virtual repo",
            excludes_pattern="com/google/**",
            external_dependencies_enabled=True,
            external_dependencies_patterns=[
                "**/github.com/**",
                "**/go.googlesource.com/**",
            ],
            includes_pattern="com/jfrog/**,cloud/jfrog/**",
            key="baz-go",
            notes="Internal description",
            repo_layout_ref="go-default",
            repositories=[])
        ```

        ## Import

        Virtual repositories can be imported using their name, e.g.

        ```sh
         $ pulumi import artifactory:index/goRepository:GoRepository foo foo
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] excludes_pattern: List of artifact patterns to exclude when evaluating artifact requests, in the form of x/y/**/z/*.By default no
               artifacts are excluded.
        :param pulumi.Input[bool] external_dependencies_enabled: . Shorthand for "Enable 'go-import' Meta Tags" on the UI. This must be set to true in order to use the allow list
        :param pulumi.Input[Sequence[pulumi.Input[str]]] external_dependencies_patterns: - 'go-import' Allow List on the UI.
        :param pulumi.Input[str] includes_pattern: List of artifact patterns to include when evaluating artifact requests in the form of x/y/**/z/*. When used, only
               artifacts matching one of the include patterns are served. By default, all artifacts are included (**/*).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GoRepositoryArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## # Artifactory Virtual Go Repository Resource

        Provides an Artifactory virtual repository resource, but with specific go lang features. This should be preferred over the original
        one-size-fits-all `VirtualRepository`.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_artifactory as artifactory

        baz_go = artifactory.GoRepository("baz-go",
            description="A test virtual repo",
            excludes_pattern="com/google/**",
            external_dependencies_enabled=True,
            external_dependencies_patterns=[
                "**/github.com/**",
                "**/go.googlesource.com/**",
            ],
            includes_pattern="com/jfrog/**,cloud/jfrog/**",
            key="baz-go",
            notes="Internal description",
            repo_layout_ref="go-default",
            repositories=[])
        ```

        ## Import

        Virtual repositories can be imported using their name, e.g.

        ```sh
         $ pulumi import artifactory:index/goRepository:GoRepository foo foo
        ```

        :param str resource_name: The name of the resource.
        :param GoRepositoryArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GoRepositoryArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 artifactory_requests_can_retrieve_remote_artifacts: Optional[pulumi.Input[bool]] = None,
                 default_deployment_repo: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 excludes_pattern: Optional[pulumi.Input[str]] = None,
                 external_dependencies_enabled: Optional[pulumi.Input[bool]] = None,
                 external_dependencies_patterns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 includes_pattern: Optional[pulumi.Input[str]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 repo_layout_ref: Optional[pulumi.Input[str]] = None,
                 repositories: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GoRepositoryArgs.__new__(GoRepositoryArgs)

            __props__.__dict__["artifactory_requests_can_retrieve_remote_artifacts"] = artifactory_requests_can_retrieve_remote_artifacts
            __props__.__dict__["default_deployment_repo"] = default_deployment_repo
            __props__.__dict__["description"] = description
            __props__.__dict__["excludes_pattern"] = excludes_pattern
            __props__.__dict__["external_dependencies_enabled"] = external_dependencies_enabled
            __props__.__dict__["external_dependencies_patterns"] = external_dependencies_patterns
            __props__.__dict__["includes_pattern"] = includes_pattern
            if key is None and not opts.urn:
                raise TypeError("Missing required property 'key'")
            __props__.__dict__["key"] = key
            __props__.__dict__["notes"] = notes
            __props__.__dict__["repo_layout_ref"] = repo_layout_ref
            if repositories is None and not opts.urn:
                raise TypeError("Missing required property 'repositories'")
            __props__.__dict__["repositories"] = repositories
            __props__.__dict__["package_type"] = None
        super(GoRepository, __self__).__init__(
            'artifactory:index/goRepository:GoRepository',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            artifactory_requests_can_retrieve_remote_artifacts: Optional[pulumi.Input[bool]] = None,
            default_deployment_repo: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            excludes_pattern: Optional[pulumi.Input[str]] = None,
            external_dependencies_enabled: Optional[pulumi.Input[bool]] = None,
            external_dependencies_patterns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            includes_pattern: Optional[pulumi.Input[str]] = None,
            key: Optional[pulumi.Input[str]] = None,
            notes: Optional[pulumi.Input[str]] = None,
            package_type: Optional[pulumi.Input[str]] = None,
            repo_layout_ref: Optional[pulumi.Input[str]] = None,
            repositories: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'GoRepository':
        """
        Get an existing GoRepository resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] excludes_pattern: List of artifact patterns to exclude when evaluating artifact requests, in the form of x/y/**/z/*.By default no
               artifacts are excluded.
        :param pulumi.Input[bool] external_dependencies_enabled: . Shorthand for "Enable 'go-import' Meta Tags" on the UI. This must be set to true in order to use the allow list
        :param pulumi.Input[Sequence[pulumi.Input[str]]] external_dependencies_patterns: - 'go-import' Allow List on the UI.
        :param pulumi.Input[str] includes_pattern: List of artifact patterns to include when evaluating artifact requests in the form of x/y/**/z/*. When used, only
               artifacts matching one of the include patterns are served. By default, all artifacts are included (**/*).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GoRepositoryState.__new__(_GoRepositoryState)

        __props__.__dict__["artifactory_requests_can_retrieve_remote_artifacts"] = artifactory_requests_can_retrieve_remote_artifacts
        __props__.__dict__["default_deployment_repo"] = default_deployment_repo
        __props__.__dict__["description"] = description
        __props__.__dict__["excludes_pattern"] = excludes_pattern
        __props__.__dict__["external_dependencies_enabled"] = external_dependencies_enabled
        __props__.__dict__["external_dependencies_patterns"] = external_dependencies_patterns
        __props__.__dict__["includes_pattern"] = includes_pattern
        __props__.__dict__["key"] = key
        __props__.__dict__["notes"] = notes
        __props__.__dict__["package_type"] = package_type
        __props__.__dict__["repo_layout_ref"] = repo_layout_ref
        __props__.__dict__["repositories"] = repositories
        return GoRepository(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="artifactoryRequestsCanRetrieveRemoteArtifacts")
    def artifactory_requests_can_retrieve_remote_artifacts(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "artifactory_requests_can_retrieve_remote_artifacts")

    @property
    @pulumi.getter(name="defaultDeploymentRepo")
    def default_deployment_repo(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "default_deployment_repo")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="excludesPattern")
    def excludes_pattern(self) -> pulumi.Output[Optional[str]]:
        """
        List of artifact patterns to exclude when evaluating artifact requests, in the form of x/y/**/z/*.By default no
        artifacts are excluded.
        """
        return pulumi.get(self, "excludes_pattern")

    @property
    @pulumi.getter(name="externalDependenciesEnabled")
    def external_dependencies_enabled(self) -> pulumi.Output[bool]:
        """
        . Shorthand for "Enable 'go-import' Meta Tags" on the UI. This must be set to true in order to use the allow list
        """
        return pulumi.get(self, "external_dependencies_enabled")

    @property
    @pulumi.getter(name="externalDependenciesPatterns")
    def external_dependencies_patterns(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        - 'go-import' Allow List on the UI.
        """
        return pulumi.get(self, "external_dependencies_patterns")

    @property
    @pulumi.getter(name="includesPattern")
    def includes_pattern(self) -> pulumi.Output[Optional[str]]:
        """
        List of artifact patterns to include when evaluating artifact requests in the form of x/y/**/z/*. When used, only
        artifacts matching one of the include patterns are served. By default, all artifacts are included (**/*).
        """
        return pulumi.get(self, "includes_pattern")

    @property
    @pulumi.getter
    def key(self) -> pulumi.Output[str]:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def notes(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "notes")

    @property
    @pulumi.getter(name="packageType")
    def package_type(self) -> pulumi.Output[str]:
        return pulumi.get(self, "package_type")

    @property
    @pulumi.getter(name="repoLayoutRef")
    def repo_layout_ref(self) -> pulumi.Output[str]:
        return pulumi.get(self, "repo_layout_ref")

    @property
    @pulumi.getter
    def repositories(self) -> pulumi.Output[Sequence[str]]:
        return pulumi.get(self, "repositories")

