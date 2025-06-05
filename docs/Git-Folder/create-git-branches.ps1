$branches = @(
    "testing",
    "feature/merging",
    "final",
    "experiment",
    "category/ambulance",
    "category/bedsideattendent",
    "category/bloodbank",
    "category/motherandbaby",
    "category/nursing",
    "category/pregnancy"
)

foreach ($branch in $branches) {
    if (git branch --list $branch) {
        Write-Host "⚠️ Branch '$branch' already exists, skipping."
    }
    else {
        git branch $branch
        Write-Host "✅ Branch '$branch' created."
    }
}

Write-Host "`n🎉 All branches created or already existed."
