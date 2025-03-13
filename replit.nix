{pkgs}: {
  deps = [
    pkgs.python312Packages.pyngrok
    pkgs.postgresql
    pkgs.openssl
  ];
}
