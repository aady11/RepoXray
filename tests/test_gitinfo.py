from __future__ import annotations

import unittest

from repoxray.gitinfo import _sanitize_remote_url


class RemoteUrlSanitizationTests(unittest.TestCase):
    def test_removes_https_user_info_and_query_parameters(self) -> None:
        remote = "https://user:super-secret-token@github.com/aady11/RepoXray.git?access_token=another-secret"
        sanitized = _sanitize_remote_url(remote)
        self.assertEqual(sanitized, "https://github.com/aady11/RepoXray.git")
        self.assertNotIn("super-secret-token", sanitized)
        self.assertNotIn("another-secret", sanitized)

    def test_removes_ssh_url_user_info(self) -> None:
        self.assertEqual(
            _sanitize_remote_url("ssh://git:secret@github.com/aady11/RepoXray.git"),
            "ssh://github.com/aady11/RepoXray.git",
        )

    def test_removes_scp_style_user_info(self) -> None:
        self.assertEqual(
            _sanitize_remote_url("git:secret@github.com:aady11/RepoXray.git"),
            "github.com:aady11/RepoXray.git",
        )

    def test_preserves_plain_scp_style_remote(self) -> None:
        self.assertEqual(
            _sanitize_remote_url("git@github.com:aady11/RepoXray.git"),
            "github.com:aady11/RepoXray.git",
        )

    def test_preserves_local_path_remote(self) -> None:
        self.assertEqual(_sanitize_remote_url("../RepoXray.git"), "../RepoXray.git")


if __name__ == "__main__":
    unittest.main()
